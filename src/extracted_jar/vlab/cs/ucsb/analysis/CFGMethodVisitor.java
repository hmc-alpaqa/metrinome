package vlab.cs.ucsb.analysis;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.MethodNode;
import org.objectweb.asm.tree.analysis.Analyzer;
import org.objectweb.asm.tree.analysis.AnalyzerException;
import org.objectweb.asm.tree.analysis.BasicInterpreter;
import org.objectweb.asm.tree.analysis.Frame;

import vlab.cs.ucsb.ComOptions;
import vlab.cs.ucsb.db.SqliteJDBC;

public class CFGMethodVisitor extends MethodVisitor {
	public String mAccess;
	public String mOwner;
	public String mName;
	public String mDesc;
	
	MethodVisitor next;
	
	public static Map<String, Integer> mIndexes = new HashMap<String, Integer>();
	
	public static int keyIndex = 1;
	public static Map<Frame, Integer> keys = new HashMap<Frame, Integer>();
	
	public static int basicKeyIndex = 1;
	public static Map<BasicBlock, Integer> basicKeys = new HashMap<BasicBlock, Integer>();
	
	public CFGMethodVisitor(MethodVisitor mv, int access, String owner, String name, String desc) {
		super(Opcodes.ASM5, new MethodNode(access, name, desc, null, null));
		mAccess = Integer.toString(access);
		mOwner = owner;
		mName = name;
		mDesc = desc;
		next = mv;
	}

	@Override
	public void visitEnd() {
		if (mIndexes.containsKey(mName)) {
			mIndexes.put(mName, mIndexes.get(mName) + 1);
		}
		
		MethodNode mn = (MethodNode) mv;
		
		Analyzer a = new Analyzer(new BasicInterpreter()) {

			@Override
			protected void newControlFlowEdge(int src, int dst) {
				Node s = (Node) getFrames()[src];
				Node t = (Node)getFrames()[dst];
				s.successors.add(t);
				t.predecessors.add(s);
			}

			@Override
			protected Frame newFrame(Frame src) {
				return new Node(src);
			}

			@Override
			protected Frame newFrame(int nLocals, int nStack) {
				return new Node(nLocals, nStack);
			}
			
		};
		
		
		try {
			a.analyze(mOwner, mn);

			
			Frame[] frames = a.getFrames();
						
//			String outFile = ComOptions.OUTPUT_FOLDER_PATH + "/" + mOwner.replace("/", "_") + "_" + mName + "_" + getKey(mName) + ".dot";
//			PrintWriter writer = new PrintWriter(outFile, "UTF-8");
//			writer.println("digraph {");
//			writer.println("0 [label=\"START\"]");
//			int exitNode = frames.length + 1;
//			writer.println(exitNode + " [label=\"EXIT\"]");
//
//			int edges = 0;
//			int nodes = 0;
//			
//
//			for (int i = 0; i < frames.length; i++) {
//				if (frames[i] != null) {
//					edges += ((Node)frames[i]).successors.size();
//					nodes += 1;
//					
//					if (((Node)frames[i]).predecessors.size() == 0) {
//						writer.println(String.format("%s -> %s", "0", getKey(frames[i])));
//					}
//					
//					if (((Node)frames[i]).successors.size() == 0) {
//						writer.println(String.format("%s -> %s", getKey(frames[i]), exitNode));
//					}
//					
//					for ( Node succ : ((Node)frames[i]).successors ) {
//						writer.println(String.format("%s -> %s", getKey(frames[i]), getKey(succ)));
//					}
//					
//				}
//			}
//		
//			
//			
//			writer.println("}");
//			writer.close();
			
			
			
			List<BasicBlock> basicBlocks = getBasicBlocks(frames);
			
			String outFile2 = ComOptions.OUTPUT_FOLDER_PATH + "/" + mOwner.replace("/", "_") + "_" + mName + "_" + getKey(mName) + "_basic.dot";
			if (outFile2.length() > 190) {
				String owner = "" + mOwner.hashCode();
				if (owner.length() > 15) {
					owner = mOwner.substring(0, 15).replace("/", "_") + owner;
				}
				outFile2 = ComOptions.OUTPUT_FOLDER_PATH + "/" +  owner + "_" + mName + "_" + getKey(mName) + "_basic.dot";
			}
			PrintWriter writer2 = new PrintWriter(outFile2, "UTF-8");
			writer2.println("digraph {");
			
			writer2.println("0 [label=\"START\"]");
			int exitBlock = basicBlocks.size() + 1;
			writer2.println(exitBlock + " [label=\"EXIT\"]");
			boolean sinkComputed = false;
			for (BasicBlock b : basicBlocks) {
				if (b.predecessors.size() == 0 || b.isRoot) {
					writer2.println(String.format("%s -> %s", "0", getKey(b)));
				}
				
				if (b.successors.size() == 0 || (b.successors.size() == 1 && b == b.successors.iterator().next())) {
					writer2.println(String.format("%s -> %s", getKey(b), exitBlock));
					sinkComputed = true;
				}
				
				for ( BasicBlock n : b.successors ) {
					writer2.println(String.format("%s -> %s", getKey(b), getKey(n)));
				}
			}
			
			
			
			writer2.println("}");
			writer2.close();
			
			if (ComOptions.DB_MODE) {
				SqliteJDBC.updateMethod(ComOptions.DB_METHOD_ID, "dotfile", outFile2);
			}
			
			
//			int cyclo = edges - nodes + 2;
//			System.out.println(mOwner + "." + mName + ": cyclo complx --> " + cyclo);
			System.out.println(mOwner + "." + mName + ": frames --> " +  frames.length + ": basic blocks --> " + basicBlocks.size());
			
		} catch (AnalyzerException e) {
			e.printStackTrace();
			System.exit(0);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			System.exit(0);
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
			System.exit(0);
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
		
		
		resetKeyMap();
		mn.accept(next);
	}
	
	public static String getKey(String s) {
		Integer index = 0;
		if (mIndexes.containsKey(s)) {
			index = mIndexes.get(s);
		} else {
			mIndexes.put(s, index);
		}
		return index.toString();
	}
	
	public static String getKey(Frame f) {
		
		System.out.println(f + " ---> " + keyIndex);
		if (! keys.containsKey(f)) {
			keys.put(f, keyIndex++);
		}
		
		return keys.get(f).toString();
	}
	
	public static String getKey(BasicBlock b) {
		
		if (! basicKeys.containsKey(b)) {
			basicKeys.put(b, basicKeyIndex++);
		}
		
		return basicKeys.get(b).toString();
	}
	
	public static void resetKeyMap() {
		keys.clear();
		keyIndex = 1;
		basicKeys.clear();
		basicKeyIndex = 1;
		mIndexes.clear();
	}
	
	public static List<BasicBlock> getBasicBlocks(Frame[] frames) {
		
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
