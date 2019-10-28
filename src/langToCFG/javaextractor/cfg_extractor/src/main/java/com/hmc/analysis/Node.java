package com.hmc.analysis;

import java.util.HashSet;
import java.util.Set;
import org.objectweb.asm.tree.analysis.Frame;

class Node extends Frame
{
    boolean isRoot;
    Set<Node> successors;
    Set<Node> predecessors;
    
    Node(final int nLocals, final int nStack) {
        super(nLocals, nStack);
        this.isRoot = false;
        this.successors = new HashSet<>();
        this.predecessors = new HashSet<>();
    }
    
    Node(final Frame src) {
        super(src);
        this.isRoot = false;
        this.successors = new HashSet<>();
        this.predecessors = new HashSet<>();
    }
}
