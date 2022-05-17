package com.hmc.analysis;

import java.io.File;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.*;

import com.hmc.ComOptions;
import java.io.PrintWriter;

import org.objectweb.asm.tree.analysis.Analyzer;
import org.objectweb.asm.tree.analysis.BasicInterpreter;
import org.objectweb.asm.tree.MethodNode;
import org.objectweb.asm.tree.analysis.Frame;
import org.objectweb.asm.MethodVisitor;

import java.io.OutputStreamWriter;

public class CFGMethodVisitor extends MethodVisitor
{

    private String mOwner;
    private String mName;
    private MethodVisitor next;
    private static Map<String, Integer> mIndexes;
    private static int basicKeyIndex;
    private static Map<BasicBlock, Integer> basicKeys;
    
    static {
        CFGMethodVisitor.mIndexes = new HashMap<>();
        CFGMethodVisitor.basicKeyIndex = 1;
        CFGMethodVisitor.basicKeys = new HashMap<>();
    }
    
    CFGMethodVisitor(final MethodVisitor mv, final int access, final String owner, final String name, final String desc) {
        super(327680, new MethodNode(access, name, desc, null, null));
        this.mOwner = owner;
        this.mName = name;
        this.next = mv;
    }

    public void visitEnd() {
        if (CFGMethodVisitor.mIndexes.containsKey(this.mName))
            CFGMethodVisitor.mIndexes.put(this.mName, CFGMethodVisitor.mIndexes.get(this.mName) + 1);
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
            String outFile = Paths.get(String.valueOf(ComOptions.OUTPUT_FOLDER_PATH),
                    this.mOwner.replace("/", "_") + "_" + this.mName + "_" + getKey(this.mName)
                    + "_basic.dot").toString();
            System.out.println("OUTPUT FOLDER PATH: " + String.valueOf(ComOptions.OUTPUT_FOLDER_PATH));
            if (outFile.length() > 190) {
                String owner = Integer.toString(this.mOwner.hashCode());
                if (owner.length() > 15)
                    owner = String.valueOf(this.mOwner.substring(0, 15).replace("/", "_")) + owner;
                outFile = String.valueOf(ComOptions.OUTPUT_FOLDER_PATH) + "/" + owner + "_" + this.mName + "_" +
                           getKey(this.mName) + "_basic.dot";
            }

            System.out.println("Trying to create file: " + outFile);
            outFile = outFile.replace("<", "");
            outFile = outFile.replace(">", "");
            File file = new File(outFile);
            // Create all parent directories.
            System.out.println("Trying to create file: " + outFile);
            File directory = file.getParentFile();
            if (directory.exists())
                System.out.println("Directory already exists... will output to it!");
            else {
                boolean ok = directory.mkdirs();
                if (!ok)
                    System.out.println("Could not create parent dirs.");
                ok = file.createNewFile();
                if (!ok)
                    System.out.println("Could not create file");
            }

            final PrintWriter writer = new PrintWriter(
                    new OutputStreamWriter(new FileOutputStream(outFile), StandardCharsets.UTF_8),true
            );
            writer.println("digraph {");
            writer.println("0 [label=\"START\"]");
            final int exitBlock = basicBlocks.size() + 1;
            writer.println(String.valueOf(exitBlock) + " [label=\"EXIT\"]");
            for (final BasicBlock b : basicBlocks) {
                if (b.predecessors.size() == 0 || b.isRoot)
                    writer.println(String.format("%s -> %s", "0", getKey(b)));

                if (b.successors.size() == 0 || (b.successors.size() == 1 && b == b.successors.iterator().next()))
                    writer.println(String.format("%s -> %s", getKey(b), exitBlock));

                for (final BasicBlock n : b.successors)
                    writer.println(String.format("%s -> %s", getKey(b), getKey(n)));

            }
            writer.println("}");
            writer.close();
            System.out.println(String.valueOf(this.mOwner) + "." + this.mName + ": frames --> " +
                               frames.length + ": basic blocks --> " + basicBlocks.size());
        }
        catch (Exception e) {
            e.printStackTrace();
            System.exit(0);
        }
        resetKeyMap();
        mn.accept(this.next);
    }
    
    private static String getKey(final String s) {
        Integer index = 0;
        if (CFGMethodVisitor.mIndexes.containsKey(s))
            index = CFGMethodVisitor.mIndexes.get(s);
        else
            CFGMethodVisitor.mIndexes.put(s, index);
        return index.toString();
    }

    private static String getKey(final BasicBlock b) {
        if (!CFGMethodVisitor.basicKeys.containsKey(b))
            CFGMethodVisitor.basicKeys.put(b, CFGMethodVisitor.basicKeyIndex++);
        return CFGMethodVisitor.basicKeys.get(b).toString();
    }
    
    private static void resetKeyMap() {
        CFGMethodVisitor.basicKeys.clear();
        CFGMethodVisitor.basicKeyIndex = 1;
        CFGMethodVisitor.mIndexes.clear();
    }

    private static List<BasicBlock> getBasicBlocks(Frame[] frames) {

        List< Node > leaders = new ArrayList< Node >();

        for (int i = 0; i < frames.length; i++) {
            if (frames[i] != null) {
                Node n = (Node)frames[i];

                if (i == 0) {													// roots are always leaders first element is root
                    n.isRoot = true;
                    leaders.add(n);
                } else if (n.predecessors.size() == 0) {						// roots are always leaders, can be in a catch block
                    leaders.add(n);
                } else if (n.predecessors.size() > 1) { 						// if ...goto L or goto L, L is a leader
                    leaders.add(n);
                } else {														// if ...goto B or goto B, L follows that immediately, L is leader
                    for (Node p : n.predecessors) {
                        if (p.successors.size() > 1) {
                            leaders.add(n);
                        }
                    }
                }
            }
        }

        System.out.println("leaders size: " + leaders.size());

        Map<Node, BasicBlock> node2block = new HashMap<Node, BasicBlock>();
        List<BasicBlock> basicBlocks = new ArrayList<BasicBlock>();

        for (Node leader : leaders) {
            BasicBlock currBlock = null;
            if (node2block.containsKey(leader)) {
                currBlock = node2block.get(leader);
            } else {
                currBlock = new BasicBlock();
                basicBlocks.add(currBlock);
                node2block.put(leader, currBlock);
                if (leader.isRoot) {
                    currBlock.isRoot = true;
                }
            }

            Iterator<Node> it = leader.successors.iterator();
            while (it.hasNext()) {
                Node n = it.next();
                if (leaders.contains(n)) {
                    if (node2block.containsKey(n)) {
                        BasicBlock nextBlock = node2block.get(n);
                        currBlock.successors.add(nextBlock);
                        nextBlock.predecessors.add(currBlock);
                    } else {
                        BasicBlock nextBlock = new BasicBlock();
                        basicBlocks.add(nextBlock);
                        currBlock.successors.add(nextBlock);
                        nextBlock.predecessors.add(currBlock);
                        node2block.put(n, nextBlock);
                    }


                } else {
                    node2block.put(n, currBlock);
                    it = n.successors.iterator();
                }
            }

            System.out.println("basic block size: " + basicBlocks.size());
        }
        return basicBlocks;
    }
}
