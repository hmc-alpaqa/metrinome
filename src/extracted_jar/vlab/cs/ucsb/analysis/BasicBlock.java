package vlab.cs.ucsb.analysis;

import java.util.HashSet;
import java.util.Set;

import org.objectweb.asm.tree.analysis.Frame;

public class BasicBlock {
	public boolean isRoot = false;
	Set< BasicBlock > successors = new HashSet< BasicBlock >();
	Set< BasicBlock > predecessors = new HashSet< BasicBlock >();
}
