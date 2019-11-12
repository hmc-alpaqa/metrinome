package com.hmc;

import com.hmc.analysis.CFGClassVisitor;
import org.apache.commons.cli.HelpFormatter;

import java.util.ArrayList;
import java.util.Collection;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import java.io.IOException;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.ClassReader;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.DirectoryFileFilter;
import org.apache.commons.io.filefilter.RegexFileFilter;
import java.io.File;
import java.util.List;

import com.hmc.db.SqliteJDBC;
import org.apache.commons.cli.PosixParser;
import org.apache.commons.cli.Options;

public class Extractor
{
    public static void main(final String[] args) {
        // Parse command line options
        final Options comOptions = new Options();
        comOptions.addOption("p", "package-name", true, "application package name");
        comOptions.addOption("d", "database", true, "database url");
        comOptions.addOption("s", "session", true, "user session identifier");
        comOptions.addOption("m", "method", true, "db id of the method to analyze");
        comOptions.addOption("i", "input-classes", true, "folder of classes to be instrumented");
        comOptions.addOption("o", "output-folder", true, "output graphs");
        comOptions.addOption("h", "help", false, "list available options");
        final CommandLineParser comParser = new PosixParser();
        CommandLine com = null;
        try {
            com = comParser.parse(comOptions, args);
        }
        catch (Exception e2) {
            exit(comOptions);
        }
        if (com.hasOption('h')) {
            exit(comOptions);
        }
        if (com.hasOption('i')) {
            ComOptions.INPUT_CLASS_FOLDER_PATH = com.getOptionValue('i');
        }
        if (com.hasOption('o')) {
            ComOptions.OUTPUT_FOLDER_PATH = com.getOptionValue('o');
        }
        if (com.hasOption('p')) {
            ComOptions.PACKAGE_NAME = com.getOptionValue('p');
        }
        if (com.hasOption('s')) {
            ComOptions.USER_SESSION = com.getOptionValue('s');
        }
        if (com.hasOption('d')) {
            ComOptions.DB_URL = com.getOptionValue('d');
            ComOptions.DB_MODE = true;
            SqliteJDBC.connect(ComOptions.DB_URL);
        }
        if (com.hasOption('m')) {
            ComOptions.DB_METHOD_ID = com.getOptionValue('m');
            ComOptions.SINGLE_METHOD_MODE = true;
            SqliteJDBC.select(ComOptions.DB_METHOD_ID);
        }

        final File classFolder = new File(ComOptions.INPUT_CLASS_FOLDER_PATH);
        final File instrumentedClassFolder = new File(ComOptions.OUTPUT_FOLDER_PATH);
        ConsoleMessage.info("input classes folder -> " + classFolder);
        ConsoleMessage.info("output folder -> " + instrumentedClassFolder);

        // classFolder can either be a single file or a directory
        System.out.println("Working directory = " + System.getProperty("user.dir"));
        final Collection<File> classFiles;
        if (classFolder.isDirectory()) {
            classFiles = FileUtils.listFiles(
                    classFolder, new RegexFileFilter("[^\\s]+\\.class$"),
                    DirectoryFileFilter.DIRECTORY
            );
        } else {
            classFiles = new ArrayList<>();
            ((ArrayList<File>) classFiles).add(0, classFolder);
        }

        for (final File classFile : classFiles) {
            try {
                final byte[] inBytes = FileUtils.readFileToByteArray(classFile);
                final ClassReader cr = new ClassReader(inBytes);
                if (ComOptions.DB_MODE) {
                    if (!ComOptions.SINGLE_METHOD_MODE) {
                        ClassVisitor cv;
                        final ClassWriter cw = new ClassWriter(1);
                        cv = new CFGClassVisitor(cw);
                        cr.accept(cv, 0);
                    }
                    else {
                        if (cr.getClassName().equals(ComOptions.M_OWNER)) {
                            ClassVisitor cv;
                            final ClassWriter cw = new ClassWriter(1);
                            cv = new CFGClassVisitor(cw);
                            cr.accept(cv, 0);
                            break;
                        }
                    }
                }
                else {
                    ClassVisitor cv;
                    final ClassWriter cw = new ClassWriter(1);
                    cv = new CFGClassVisitor(cw);
                    cr.accept(cv, 0);
                }
            }
            catch (IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }
        }
        SqliteJDBC.close();
    }
    
    private static void exit(final Options options) {
        final HelpFormatter helpFormatter = new HelpFormatter();
        helpFormatter.printHelp("Available command line options", options, true);
        System.exit(0);
    }
}
