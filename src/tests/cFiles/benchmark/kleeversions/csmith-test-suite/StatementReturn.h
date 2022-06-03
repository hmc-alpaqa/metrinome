// -*- mode: C++ -*-
//
// Copyright (c) 2007, 2008, 2010, 2011, 2015 The University of Utah
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

#ifndef STATEMENT_RETURN_H
#define STATEMENT_RETURN_H

///////////////////////////////////////////////////////////////////////////////

#include <ostream>

#include "Statement.h"
#include "ExpressionVariable.h"

class CGContext;
class Variable;
class Function;
class FactMgr;

/*
 *
 */
class StatementReturn : public Statement
{
public:
	// Factory method.
	static StatementReturn *make_random(CGContext &cg_context);

	StatementReturn(Block* b, const ExpressionVariable &v);
	StatementReturn(const StatementReturn &sr);
	virtual ~StatementReturn(void);

	virtual void Output(std::ostream &out, FactMgr* fm, int indent = 0) const;

	virtual bool must_return(void) const {return true;}

	virtual bool must_jump(void) const {return true;}

	virtual std::vector<const ExpressionVariable*> get_dereferenced_ptrs(void) const;

	virtual void get_blocks(std::vector<const Block*>& /* blks */) const {};
	virtual void get_exprs(std::vector<const Expression*>& exps) const {exps.push_back(&var);}

	virtual bool visit_facts(vector<const Fact*>& inputs, CGContext& cg_context) const;

    const ExpressionVariable* get_var(void) const { return &var;};

private:
	const ExpressionVariable &var;
	//

	StatementReturn &operator=(const StatementReturn &sr); // unimplementable
};

///////////////////////////////////////////////////////////////////////////////

#endif // STATEMENT_RETURN_H

// Local Variables:
// c-basic-offset: 4
// tab-width: 4
// End:

// End of file.
