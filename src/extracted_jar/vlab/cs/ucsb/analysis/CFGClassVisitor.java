package vlab.cs.ucsb.analysis;

import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;

import vlab.cs.ucsb.ComOptions;
import vlab.cs.ucsb.db.SqliteJDBC;

public class CFGClassVisitor extends ClassVisitor {

	public String klass;
	public boolean isInterface;
	
	public CFGClassVisitor(ClassVisitor cv) {
		super(Opcodes.ASM5, cv);
	}

	@Override
	public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
		klass = name;
		isInterface = (access & Opcodes.ACC_INTERFACE) != 0;
		super.visit(version, access, name, superName, signature, interfaces);
	}

	@Override
	public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
		MethodVisitor mv;
		
		mv = cv.visitMethod(access, name, desc, desc, exceptions);
		boolean isAbstract = (access & Opcodes.ACC_ABSTRACT) != 0;
		boolean isNative = (access & Opcodes.ACC_NATIVE) != 0;
		if (!isInterface && !isAbstract && !isNative && mv != null) {	
			if (ComOptions.DB_MODE) {
				if (ComOptions.SINGLE_METHOD_MODE && filter(access, klass, name, desc)) {
					mv = new CFGMethodVisitor(mv, access, klass, name, desc);
				} else {
					SqliteJDBC.insertMethod(ComOptions.USER_SESSION, access, klass, name, desc, "");
				}
			} else {
				mv = new CFGMethodVisitor(mv, access, klass, name, desc);
			}
		}
		return mv;
	}
	
	public boolean filter(int access, String owner, String name, String desc) {
		if ( !ComOptions.M_NAME.equals(name) ) {
			return false;
		}
		
		if ( !ComOptions.M_DESCRIPTION.equals(desc) ) {
			return false;
		}
		
		if ( !(ComOptions.M_ACCESS_CODE == access) ) {
			return false;
		}
		
		if ( !ComOptions.M_OWNER.equals(owner) ) {
			return false;
		}
		
		return true;
	}
}
