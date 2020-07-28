package com.hmc.analysis;

import java.io.File;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;

import com.hmc.ComOptions;
import com.hmc.db.SqliteJDBC;
import java.io.PrintWriter;

import org.objectweb.asm.tree.analysis.Analyzer;
import org.objectweb.asm.tree.analysis.BasicInterpreter;
import org.objectweb.asm.tree.MethodNode;
import java.util.HashMap;
import org.objectweb.asm.tree.analysis.Frame;
import java.util.Map;
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
            String outFile2 = Paths.get(String.valueOf(ComOptions.OUTPUT_FOLDER_PATH),
                    this.mOwner.replace("/", "_") + "_" + this.mName + "_" + getKey(this.mName)
                    + "_basic.dot").toString();
            System.out.println("OUTPUT FOLDER PATH: " + String.valueOf(ComOptions.OUTPUT_FOLDER_PATH));
            if (outFile2.length() > 190) {
                String owner = Integer.toString(this.mOwner.hashCode());
                if (owner.length() > 15) {
                    owner = String.valueOf(this.mOwner.substring(0, 15).replace("/", "_")) + owner;
                }
                outFile2 = String.valueOf(ComOptions.OUTPUT_FOLDER_PATH) + "/" + owner + "_" + this.mName + "_" +
                           getKey(this.mName) + "_basic.dot";
            }

            // TODO(gbessler): fix this
            System.out.println("Trying to create file: " + outFile2);
            outFile2 = outFile2.replace("<", "");
            outFile2 = outFile2.replace(">", "");
            File file = new File(outFile2);
            // Create all parent directories.
            System.out.println("Trying to create file: " + outFile2);
            File directory = file.getParentFile();
            if (directory.exists()) {
                System.out.println("Directory already exists... will output to it!");
            } else {
                boolean ok = directory.mkdirs();
                if (!ok)
                    System.out.println("Could not create parent dirs.");
                ok = file.createNewFile();
                if (!ok)
                    System.out.println("Could not create file");
            }

            final PrintWriter writer2 = new PrintWriter(
                    new OutputStreamWriter(new FileOutputStream(outFile2), StandardCharsets.UTF_8),true
            );
            writer2.println("digraph {");
            writer2.println("0 [label=\"START\"]");
            final int exitBlock = basicBlocks.size() + 1;
            writer2.println(String.valueOf(exitBlock) + " [label=\"EXIT\"]");
            for (final BasicBlock b : basicBlocks) {
                if (b.predecessors.size() == 0 || b.isRoot)
                    writer2.println(String.format("%s -> %s", "0", getKey(b)));

                if (b.successors.size() == 0 || (b.successors.size() == 1 && b == b.successors.iterator().next()))
                    writer2.println(String.format("%s -> %s", getKey(b), exitBlock));

                for (final BasicBlock n : b.successors)
                    writer2.println(String.format("%s -> %s", getKey(b), getKey(n)));

            }
            writer2.println("}");
            writer2.close();
            if (ComOptions.DB_MODE)
                SqliteJDBC.updateMethod(ComOptions.DB_METHOD_ID, "dotfile", outFile2);

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
    
    private static List<BasicBlock> getBasicBlocks(final Frame[] frames) {
        final List<Node> leaders = new ArrayList<>();
        for (int i = 0; i < frames.length; ++i) {
            if (frames[i] != null) {
                final Node n = (Node)frames[i];
                if (i == 0)
                    n.isRoot = true;

                if (i == 0 || n.predecessors.size() != 1 || n.predecessors.iterator().next().successors.size() > 1)
                    leaders.add(n);
            }
        }
        System.out.println("leaders size: " + leaders.size());
        final Map<Node, BasicBlock> node2block = new HashMap<>();
        final List<BasicBlock> basicBlocks = new ArrayList<>();
        for (final Node leader : leaders) {
            BasicBlock currBlock;
            if (node2block.containsKey(leader))
                currBlock = node2block.get(leader);
            else {
                currBlock = new BasicBlock();
                basicBlocks.add(currBlock);
                node2block.put(leader, currBlock);
                if (leader.isRoot)
                    currBlock.isRoot = true;
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
                else
                    node2block.put(n2, currBlock);
            }
            System.out.println("basic block size: " + basicBlocks.size());
        }
        return basicBlocks;
    }
}
