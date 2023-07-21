// -*- mode: C++ -*-
//
// Copyright (c) 2008, 2009, 2010, 2011 The University of Utah
// All rights reserved.
//
// This file is part of `csmith', a random generator of C programs.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//   * Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#ifndef COVERAGE_TEST_EXTENSION_H
#define COVERAGE_TEST_EXTENSION_H

#include <vector>
#include <ostream>
#include <string>
#include "AbsExtension.h"
#include "CVQualifiers.h"

class ExtensionValue;
class Constant;

class CoverageTestExtension : public AbsExtension {
	friend class ExtensionMgr;
public:
	virtual void GenerateValues();

	virtual void OutputInit(std::ostream &out);

	virtual void OutputFirstFunInvocation(std::ostream &out, FunctionInvocation *invoke);

	virtual void OutputHeader(std::ostream &out);

	virtual void OutputTail(std::ostream &out);

	virtual std::vector<ExtensionValue *> &get_values() { return values_; }

private:

	static std::string array_base_name_;

	static std::string array_index_;

	void output_array_init(std::ostream &out, int count);

	void output_decls(std::ostream &out);

	int inputs_size_;

	// used for tmp vars
	std::vector<ExtensionValue*> values_;

	// hold actual values passed to func_1
	std::vector<Constant*> test_values_;

	CoverageTestExtension(int input_size);

	~CoverageTestExtension();
};

#endif // COVERAGE_TEST_EXTENSION_H
