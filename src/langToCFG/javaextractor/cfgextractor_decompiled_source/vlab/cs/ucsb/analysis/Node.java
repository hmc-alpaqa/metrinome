package vlab.cs.ucsb.analysis;

import java.util.HashSet;
import java.util.Set;
import org.objectweb.asm.tree.analysis.Frame;

public class Node extends Frame
{
    public boolean isRoot;
    Set<Node> successors;
    Set<Node> predecessors;
    
    public Node(final int nLocals, final int nStack) {
        super(nLocals, nStack);
        this.isRoot = false;
        this.successors = new HashSet<Node>();
        this.predecessors = new HashSet<Node>();
    }
    
    public Node(final Frame src) {
        super(src);
        this.isRoot = false;
        this.successors = new HashSet<Node>();
        this.predecessors = new HashSet<Node>();
    }
}
