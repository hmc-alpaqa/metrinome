package com.hmc.analysis;

import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.ClassVisitor;

public class CFGClassVisitor extends ClassVisitor
{
    private String klass;
    private boolean isInterface;
    
    public CFGClassVisitor(final ClassVisitor cv) {
        super(327680, cv);
    }
    
    public void visit(final int version, final int access, final String name, final String signature,
                      final String superName, final String[] interfaces) {
        this.klass = name;
        this.isInterface = ((access & 0x200) != 0x0);
        super.visit(version, access, name, superName, signature, interfaces);
    }
    
    public MethodVisitor visitMethod(final int access, final String name, final String desc,
                                     final String signature, final String[] exceptions) {
        MethodVisitor mv = this.cv.visitMethod(access, name, desc, desc, exceptions);
        final boolean isAbstract = (access & 0x400) != 0x0;
        final boolean isNative = (access & 0x100) != 0x0;
        if (!this.isInterface && !isAbstract && !isNative && mv != null)
            mv = new CFGMethodVisitor(mv, access, this.klass, name, desc);
        return mv;
    }
}
