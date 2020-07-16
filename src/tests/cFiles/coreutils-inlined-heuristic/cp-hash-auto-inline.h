__attribute__((always_inline)) inline void hash_init(void);
__attribute__((always_inline)) inline void forget_all(void);
__attribute__((always_inline)) inline void forget_created(ino_t ino, dev_t dev);
__attribute__((always_inline)) inline char *remember_copied(const char *node, ino_t ino, dev_t dev);
__attribute__((always_inline)) inline char *src_to_dest_lookup(ino_t ino, dev_t dev);
