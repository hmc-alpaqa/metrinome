package vlab.cs.ucsb.test;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStream;
import java.util.*;

import org.omg.CORBA.Request;

public class ShimpleExample {

  public boolean as_long_as_it_takes = true;

  public void lazyInitialize() {
	  as_long_as_it_takes = false;
  }
  
  
  
  public void run(Object a) {
	  lazyInitialize();
	  while (true) {
	  try {
		  Object obj = a;
		  if (obj instanceof Request) { // ignore bogons
		  Request req = (Request)obj;
		  try {
			  req.ctx();
		  } catch (Throwable t) {
	
		  }
		  }
	   } catch (Exception e) {

	  }
	  }
	  }
  
//  public InputStream in;
//  
//  private void readFully(byte[] b, int off, int len) throws IOException {
//      while (len > 0) {
//          int n = in.read(b, off, len);
//          if (n == -1) {
//              throw new EOFException();
//          }
//          off += n;
//          len -= n;
//      }
//  }
  
//  public int test() {
//    int x = 100;
//    while(as_long_as_it_takes) {
//        if(x < 200) {
//            x = 100;
//        } else {
//            x = 200;
//        }
//    }
//    return x;
//  }
  
//  public boolean iftest(String s) {
//	  return s == "";
//  }
//  
//  public boolean readFully(int x) {
//	  boolean result = false;
//	  if (x > 3) {
//		  result = true;
//	  }
//	  
//	  try {
//		  if (x > 5) {
//			  result = false;
//		  }
//	} catch (Exception e) {
//		while (x > 5) {
//			if (x == 5) {
//				x--;
//			}
//		}
//	}
//	  
//	  return result;
//	  
//  }
  
//  public boolean throwtest(int x) throws Exception {
//	  boolean result = false;
//	  if (x > 3) {
//		  result = true;
//	  }
//	  
//
//	  if (x > 5) {
//		  throw new Exception("Unhandled");
//	  }
//
//
//	  
//	  if (x < 8) {
//		  result = result && true;
//	  }
//	  
//	  if (x == 4) {
//		  result = result || false;
//	  }
//	  
//	  return result;
//	  
//  }
  
//  public void test1(int x) {
//	  String result = "";
//	  if (x > 0) {
//		  result = " > 0";
//	  }
//	  
//	  if (x > 4) {
//		  result = " > 4";
//	  }
//	  
//	  if (x > 8) {
//		  result = " > 8";
//	  }
//	  
//	  System.out.println(result);
//  }
//  
//  public int test2(int x) {
//	  
//	  int r = 0;
//	  
//	  if (x < 0)
//		  if ( x < -2)
//			  if (x == -10)
//				  return -1;
//			  else 
//				  r = 10;
//	  
//	  return r;
//  }
//  
//  public String test3 (int x) {
//	  
//	  while ( x > 3) {
//		  int a = x * x;
//	  }
//	  
//	  for (int i = 0; i < x ; i++) {
//		  int z = x * 2;
//	  }
//	  
//	  int y = 0;
//	  
//	  do {
//		  y = x + 1;
//	  } while (y < 34);
//	  
//	  
//	  return "";
//  }
//  
//  public int test4(int x, int y, int z) {
//	   int result = 1;
//	   
//	   for (int i = 0; i < x; i++) {
//		   for (int j = i; j < y; j++) {
//			   for (int k = j; k < z; k++) {
//				   result = z + i + y;
//			   }
//		   }
//	   }
//	   
//	   return result;
//  }
//  
//  public void test5 (int n) {
//	  int result = 0;
//	  for(int i = 0; i < n; i++)
//		    for(int j = 0; j < n; j ++)
//		        for(int k = 0; k < n; k++)
//		             result += i*k + j;
//	  
//	  System.out.println(result);
//  }
//  
//  public void test6(int n) {
//	  int i = 0;
//	  int result = 0;
//		for(i = 0; i < n; i ++)
//		    result += i;
//		for(i = 0; i < n; i ++)
//		    result += 2*i;
//		for(i = 0; i < n; i ++)
//			result += 3*i;
//  }

}

