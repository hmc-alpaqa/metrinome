package javacfg.analysis;

import java.util.HashSet;
import java.util.Set;

public class BasicBlock
{
    public boolean isRoot;
    Set<BasicBlock> successors;
    Set<BasicBlock> predecessors;
    
    public BasicBlock() {
        this.isRoot = false;
        this.successors = new HashSet<>();
        this.predecessors = new HashSet<>();
    }
}
