package vlab.cs.ucsb.test;

import org.omg.CORBA.Request;

public class ShimpleExample
{
    public boolean as_long_as_it_takes;
    
    public ShimpleExample() {
        this.as_long_as_it_takes = true;
    }
    
    public void lazyInitialize() {
        this.as_long_as_it_takes = false;
    }
    
    public void run(final Object a) {
        this.lazyInitialize();
        while (true) {
            try {
                while (true) {
                    final Object obj = a;
                    if (obj instanceof Request) {
                        final Request req = (Request)obj;
                        try {
                            req.ctx();
                        }
                        catch (Throwable t) {}
                    }
                }
            }
            catch (Exception ex) {
                continue;
            }
            break;
        }
    }
}
