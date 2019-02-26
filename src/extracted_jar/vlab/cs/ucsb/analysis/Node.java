package vlab.cs.ucsb.analysis;

import java.util.HashSet;
import java.util.Set;

import org.objectweb.asm.tree.analysis.Frame;

public class Node extends Frame {

	public boolean isRoot = false;
	Set< Node > successors = new HashSet< Node >();
	Set< Node > predecessors = new HashSet< Node >();
	
	
	public Node(int nLocals, int nStack) {
		super(nLocals, nStack);
	}
	
	public Node(Frame src) {
		super(src);
	}
}
