package vlab.cs.ucsb.analysis;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.io.UnsupportedEncodingException;
import java.io.FileNotFoundException;
import org.objectweb.asm.tree.analysis.AnalyzerException;
import vlab.cs.ucsb.db.SqliteJDBC;
import java.io.PrintWriter;
import vlab.cs.ucsb.ComOptions;
import org.objectweb.asm.tree.analysis.Interpreter;
import org.objectweb.asm.tree.analysis.Analyzer;
import org.objectweb.asm.tree.analysis.BasicInterpreter;
import org.objectweb.asm.tree.MethodNode;
import java.util.HashMap;
import org.objectweb.asm.tree.analysis.Frame;
import java.util.Map;
import org.objectweb.asm.MethodVisitor;

public class CFGMethodVisitor extends MethodVisitor
{
    public String mAccess;
    public String mOwner;
    public String mName;
    public String mDesc;
    MethodVisitor next;
    public static Map<String, Integer> mIndexes;
    public static int keyIndex;
    public static Map<Frame, Integer> keys;
    public static int basicKeyIndex;
    public static Map<BasicBlock, Integer> basicKeys;
    
    static {
        CFGMethodVisitor.mIndexes = new HashMap<String, Integer>();
        CFGMethodVisitor.keyIndex = 1;
        CFGMethodVisitor.keys = new HashMap<Frame, Integer>();
        CFGMethodVisitor.basicKeyIndex = 1;
        CFGMethodVisitor.basicKeys = new HashMap<BasicBlock, Integer>();
    }
    
    public CFGMethodVisitor(final MethodVisitor mv, final int access, final String owner, final String name, final String desc) {
        super(327680, (MethodVisitor)new MethodNode(access, name, desc, (String)null, (String[])null));
        this.mAccess = Integer.toString(access);
        this.mOwner = owner;
        this.mName = name;
        this.mDesc = desc;
        this.next = mv;
    }
    
    public void visitEnd() {
        if (CFGMethodVisitor.mIndexes.containsKey(this.mName)) {
            CFGMethodVisitor.mIndexes.put(this.mName, CFGMethodVisitor.mIndexes.get(this.mName) + 1);
        }
        final MethodNode mn = (MethodNode)this.mv;
        final Analyzer a = new Analyzer(new BasicInterpreter()) {
            protected void newControlFlowEdge(final int src, final int dst) {
                final Node s = (Node)this.getFrames()[src];
                final Node t = (Node)this.getFrames()[dst];
                s.successors.add(t);
                t.predecessors.add(s);
            }
            
            protected Frame newFrame(final Frame src) {
                return new Node(src);
            }
            
            protected Frame newFrame(final int nLocals, final int nStack) {
                return new Node(nLocals, nStack);
            }
        };
        try {
            a.analyze(this.mOwner, mn);
            final Frame[] frames = a.getFrames();
            final List<BasicBlock> basicBlocks = getBasicBlocks(frames);
            String outFile2 = String.valueOf(ComOptions.OUTPUT_FOLDER_PATH) + "/" + this.mOwner.replace("/", "_") + "_" + this.mName + "_" + getKey(this.mName) + "_basic.dot";
            if (outFile2.length() > 190) {
                String owner = new StringBuilder().append(this.mOwner.hashCode()).toString();
                if (owner.length() > 15) {
                    owner = String.valueOf(this.mOwner.substring(0, 15).replace("/", "_")) + owner;
                }
                outFile2 = String.valueOf(ComOptions.OUTPUT_FOLDER_PATH) + "/" + owner + "_" + this.mName + "_" + getKey(this.mName) + "_basic.dot";
            }
            final PrintWriter writer2 = new PrintWriter(outFile2, "UTF-8");
            writer2.println("digraph {");
            writer2.println("0 [label=\"START\"]");
            final int exitBlock = basicBlocks.size() + 1;
            writer2.println(String.valueOf(exitBlock) + " [label=\"EXIT\"]");
            boolean sinkComputed = false;
            for (final BasicBlock b : basicBlocks) {
                if (b.predecessors.size() == 0 || b.isRoot) {
                    writer2.println(String.format("%s -> %s", "0", getKey(b)));
                }
                if (b.successors.size() == 0 || (b.successors.size() == 1 && b == b.successors.iterator().next())) {
                    writer2.println(String.format("%s -> %s", getKey(b), exitBlock));
                    sinkComputed = true;
                }
                for (final BasicBlock n : b.successors) {
                    writer2.println(String.format("%s -> %s", getKey(b), getKey(n)));
                }
            }
            writer2.println("}");
            writer2.close();
            if (ComOptions.DB_MODE) {
                SqliteJDBC.updateMethod(ComOptions.DB_METHOD_ID, "dotfile", outFile2);
            }
            System.out.println(String.valueOf(this.mOwner) + "." + this.mName + ": frames --> " + frames.length + ": basic blocks --> " + basicBlocks.size());
        }
        catch (AnalyzerException e) {
            e.printStackTrace();
            System.exit(0);
        }
        catch (FileNotFoundException e2) {
            e2.printStackTrace();
            System.exit(0);
        }
        catch (UnsupportedEncodingException e3) {
            e3.printStackTrace();
            System.exit(0);
        }
        catch (Exception e4) {
            e4.printStackTrace();
            System.exit(0);
        }
        resetKeyMap();
        mn.accept(this.next);
    }
    
    public static String getKey(final String s) {
        Integer index = 0;
        if (CFGMethodVisitor.mIndexes.containsKey(s)) {
            index = CFGMethodVisitor.mIndexes.get(s);
        }
        else {
            CFGMethodVisitor.mIndexes.put(s, index);
        }
        return index.toString();
    }
    
    public static String getKey(final Frame f) {
        System.out.println(f + " ---> " + CFGMethodVisitor.keyIndex);
        if (!CFGMethodVisitor.keys.containsKey(f)) {
            CFGMethodVisitor.keys.put(f, CFGMethodVisitor.keyIndex++);
        }
        return CFGMethodVisitor.keys.get(f).toString();
    }
    
    public static String getKey(final BasicBlock b) {
        if (!CFGMethodVisitor.basicKeys.containsKey(b)) {
            CFGMethodVisitor.basicKeys.put(b, CFGMethodVisitor.basicKeyIndex++);
        }
        return CFGMethodVisitor.basicKeys.get(b).toString();
    }
    
    public static void resetKeyMap() {
        CFGMethodVisitor.keys.clear();
        CFGMethodVisitor.keyIndex = 1;
        CFGMethodVisitor.basicKeys.clear();
        CFGMethodVisitor.basicKeyIndex = 1;
        CFGMethodVisitor.mIndexes.clear();
    }
    
    public static List<BasicBlock> getBasicBlocks(final Frame[] frames) {
        final List<Node> leaders = new ArrayList<Node>();
        for (int i = 0; i < frames.length; ++i) {
            if (frames[i] != null) {
                final Node n = (Node)frames[i];
                if (i == 0) {
                    n.isRoot = true;
                    leaders.add(n);
                }
                else if (n.predecessors.size() == 0) {
                    leaders.add(n);
                }
                else if (n.predecessors.size() > 1) {
                    leaders.add(n);
                }
                else {
                    for (final Node p : n.predecessors) {
                        if (p.successors.size() > 1) {
                            leaders.add(n);
                        }
                    }
                }
            }
        }
        System.out.println("leaders size: " + leaders.size());
        final Map<Node, BasicBlock> node2block = new HashMap<Node, BasicBlock>();
        final List<BasicBlock> basicBlocks = new ArrayList<BasicBlock>();
        for (final Node leader : leaders) {
            BasicBlock currBlock = null;
            if (node2block.containsKey(leader)) {
                currBlock = node2block.get(leader);
            }
            else {
                currBlock = new BasicBlock();
                basicBlocks.add(currBlock);
                node2block.put(leader, currBlock);
                if (leader.isRoot) {
                    currBlock.isRoot = true;
                }
            }
            for (final Node n2 : leader.successors) {
                if (leaders.contains(n2)) {
                    if (node2block.containsKey(n2)) {
                        final BasicBlock nextBlock = node2block.get(n2);
                        currBlock.successors.add(nextBlock);
                        nextBlock.predecessors.add(currBlock);
                    }
                    else {
                        final BasicBlock nextBlock = new BasicBlock();
                        basicBlocks.add(nextBlock);
                        currBlock.successors.add(nextBlock);
                        nextBlock.predecessors.add(currBlock);
                        node2block.put(n2, nextBlock);
                    }
                }
                else {
                    node2block.put(n2, currBlock);
                    final Iterator<Node> it = n2.successors.iterator();
                }
            }
            System.out.println("basic block size: " + basicBlocks.size());
        }
        return basicBlocks;
    }
}
