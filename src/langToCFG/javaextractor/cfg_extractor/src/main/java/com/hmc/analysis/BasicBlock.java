package com.hmc.analysis;

import java.util.Set;
import java.util.HashSet;

class BasicBlock
{
    boolean isRoot;
    Set<BasicBlock> successors;
    Set<BasicBlock> predecessors;
    
    BasicBlock() {
        this.isRoot = false;
        this.successors = new HashSet<>();
        this.predecessors = new HashSet<>();
    }
}
