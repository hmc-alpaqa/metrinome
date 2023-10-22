FROM scratch
# ADD file:422aca8901ae3d869a815051cea7f1e4c0204fad16884e7cd01da57d142f2e3a in / 
 CMD ["bash"]
 ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
 ENV LANG=C.UTF-8
RUN set -eux;   apt-get update;     apt-get install -y --no-install-recommends      ca-certificates         netbase         tzdata  ;   rm -rf /var/lib/apt/lists/*
 ENV GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
 ENV PYTHON_VERSION=3.9.1
RUN set -ex         && savedAptMark="$(apt-mark showmanual)"    && apt-get update && apt-get install -y --no-install-recommends         dpkg-dev        gcc         libbluetooth-dev        libbz2-dev      libc6-dev       libexpat1-dev       libffi-dev      libgdbm-dev         liblzma-dev         libncursesw5-dev        libreadline-dev         libsqlite3-dev      libssl-dev      make        tk-dev      uuid-dev        wget        xz-utils        zlib1g-dev      $(command -v gpg > /dev/null || echo 'gnupg dirmngr')       && wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz"    && wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"    && export GNUPGHOME="$(mktemp -d)"  && gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY"    && gpg --batch --verify python.tar.xz.asc python.tar.xz     && { command -v gpgconf > /dev/null && gpgconf --kill all || :; }   && rm -rf "$GNUPGHOME" python.tar.xz.asc    && mkdir -p /usr/src/python     && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz   && rm python.tar.xz         && cd /usr/src/python   && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"    && ./configure      --build="$gnuArch"      --enable-loadable-sqlite-extensions         --enable-optimizations      --enable-option-checking=fatal      --enable-shared         --with-system-expat         --with-system-ffi       --without-ensurepip     && make -j "$(nproc)"       LDFLAGS="-Wl,--strip-all"   && make install     && rm -rf /usr/src/python       && find /usr/local -depth       \(          \( -type d -a \( -name test -o -name tests -o -name idle_test \) \)             -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) \)         \) -exec rm -rf '{}' +      && ldconfig         && apt-mark auto '.*' > /dev/null   && apt-mark manual $savedAptMark    && find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec ldd '{}' ';'      | awk '/=>/ { print $(NF-1) }'      | sort -u       | xargs -r dpkg-query --search      | cut -d: -f1       | sort -u       | xargs -r apt-mark manual  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false     && rm -rf /var/lib/apt/lists/*      && python3 --version
RUN cd /usr/local/bin   && ln -s idle3 idle     && ln -s pydoc3 pydoc   && ln -s python3 python     && ln -s python3-config python-config
 ENV PYTHON_PIP_VERSION=21.0.1
 ENV PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/4be3fe44ad9dedc028629ed1497052d65d281b8e/get-pip.py
 ENV PYTHON_GET_PIP_SHA256=8006625804f55e1bd99ad4214fd07082fee27a1c35945648a58f9087a714e9d4
RUN set -ex;        savedAptMark="$(apt-mark showmanual)";  apt-get update;     apt-get install -y --no-install-recommends wget;        wget -O get-pip.py "$PYTHON_GET_PIP_URL";   echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -;       apt-mark auto '.*' > /dev/null;     [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark;    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false;   rm -rf /var/lib/apt/lists/*;        python get-pip.py       --disable-pip-version-check         --no-cache-dir      "pip==$PYTHON_PIP_VERSION"  ;   pip --version;      find /usr/local -depth      \(          \( -type d -a \( -name test -o -name tests -o -name idle_test \) \)             -o          \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \)       \) -exec rm -rf '{}' +;     rm -f get-pip.py
 CMD ["python3"]
WORKDIR /app
COPY file:fb48f3f3912f873690a962bb80a85c4cf39fe48ef9398313b9604e0b6837cdbf in /app/ 
COPY dir:528fc36ee5e674497ee5ed1cf58e6b2de7b899ce3dfc69d99a2b4354b358b6e6 in /app/examples/ 
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN mkdir -p /usr/share/man/man1 && apt-get update && apt-get install -y build-essential wget software-properties-common openjdk-11-jdk-headless
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-get update
RUN apt-get install -y curl libcap-dev git unzip doxygen libsqlite3-dev libgoogle-perftools-dev libtcmalloc-minimal4 cmake libncurses5-dev
RUN pip install tabulate
RUN apt-get install -y clang-6.0 llvm-6.0 llvm-6.0-dev llvm-6.0-tools zsh vim tmux
RUN apt-get install -y g++-multilib
RUN git clone https://github.com/Z3Prover/z3/
RUN cd /app/z3 && git pull && git reset --hard 2d1684bc2d2621c0d6b02b81168624388648049a
RUN cd /app/z3 && python scripts/mk_make.py
RUN cd /app/z3/build && make && make install
RUN pip install z3-solver
RUN pip install lit
RUN git clone https://github.com/klee/klee-uclibc.git
RUN ln -s /usr/bin/llvm-config-6.0 /usr/bin/llvm-config
RUN alias llvm-config=llvm-config-6.0
RUN CC=/usr/bin/clang-6.0 /app/klee-uclibc/configure --make-llvm-lib
RUN cd /app/klee-uclibc && make -j2
RUN mkdir /app/build
RUN git clone https://github.com/klee/klee.git
RUN apt-get install zlib1g-dev
RUN cd /app/build && cmake -DENABLE_SOLVER_STP=OFF -DENABLE_POSIX_RUNTIME=ON -DENABLE_KLEE_UCLIBC=ON -DKLEE_UCLIBC_PATH=/app/klee-uclibc -DENABLE_UNIT_TESTS=OFF -DLLVMCC=/usr/bin/clang-6.0 -ENABLE_ZLIB=OFF -DLLVMCXX=/usr/bin/clang++-6.0 /app/klee
RUN cd /app/build && make
RUN pip install wllvm
RUN curl -OL https://github.com/google/googletest/archive/release-1.7.0.zip
RUN unzip /app/release-1.7.0.zip
RUN pip install pycparser
RUN git clone https://github.com/eliben/pycparser
 ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/build/bin/
RUN git clone https://github.com/google/AFL
RUN git clone https://github.com/isstac/kelinci
RUN git clone https://github.com/rohanpadhye/jqf
RUN git clone https://github.com/javapathfinder/jpf-core
RUN git clone https://github.com/SymbolicPathFinder/jpf-symbc
RUN mkdir jpf && mv jpf-core jpf && mv jpf-symbc jpf
COPY file:d5d650313d4b67095029cb46b1a67589eb284e43a5c75cc3322c4c89c94c8b91 in /app/jpf/ 
COPY file:0e67546ba9074864acbe611321e395766f97661ae4a3fd920e27928964ae22c4 in /app/ 
RUN gunzip prism-4.5-linux64.tar.gz && tar xf prism-4.5-linux64.tar && cd prism-4.5-linux64 && ./install.sh
RUN rm -rf /app/prism-4.5-linux64.tar && rm /app/requirements.txt && rm /app/release-1.7.0.zip
RUN echo "y" | sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN mkdir /app/code/
 ENV PYTHONPATH=/app/code/
WORKDIR /app/code/