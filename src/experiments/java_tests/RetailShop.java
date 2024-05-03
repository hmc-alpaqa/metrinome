/*Retail Shop


A Retail shop wants to maintain the product availability in their shop.

Create a Class Shop with the private attributes shopName, shopAddress, products(string array). Include Constructor to initialize value for this attributes and appropriate getter and setter method if needed. 

Write the following method in the class:

boolean checkProductAvailability(String productname) - this method should take the product name as argument and check whether that product is available in the shop or not. If the product is available, function should return true, else return false.

Write the main method to test the application.

Note: Always number of products should be greater than zero. 

Sample Input 1:

Enter the shopname:
TMD
Enter the address:
Chennai
Enter number of products:

4
Laptop
Camera
Pendrive
Mobile
Enter the product to be searched:
Camera
Sample Output 1:

Product is available at TMD, Chennai.



Sample Input 2:
Enter the shopname:
TMD
Enter the address:
Chennai
Enter no of products:
4
Laptop
Camera
Pendrive
Mobile
Enter the product to be searched:
Telephone

Sample Output 2:

Product is not available at TMD, Chennai.*/

import java.util.Scanner;
import java.util.Arrays;
public class Shop
{
private String shopName;
private String shopAddress;
private String[] products;
public void setShopName(String shopName){
this.shopName=shopName;
}
public void setShopAddress(String shopAddress){
this.shopAddress=shopAddress;
}
public void setProducts(String[] products)
{
this.products=products;
}
public String getShopName(){
return this.shopName;
}
public String getShopAddress(){
return this.shopAddress;
}
public String[] getProducts(){
return this.products;
}
public Shop(String sName,String sAdd,String[] pro)
{
this.shopName=sName;
this.shopAddress=sAdd;
this.products=new String[pro.length];
System.arraycopy(pro,0,this.products,0,pro.length);
}
public boolean checkProductAvailability(String productname)
{
boolean b=false;
String products[]=getProducts();
for(int i=0;i<products.length;i++){
if(products[i].equalsIgnoreCase(productname))
{
b=true;
break;
}
}
return b;
}
public static void main (String[] args) {
Scanner s=new Scanner(System.in);
System.out.println("Enter the shopname:");
String name=s.nextLine();
System.out.println("Enter the address:");
String address=s.nextLine();
System.out.println("Enter number of products:");
int num=s.nextInt();
String[] pname=new String[num];
for(int i=0;i<num;i++)
{
pname[i]=s.next();
pname[i]+=s.nextLine();
}
Shop sh=new Shop(name,address,pname);
System.out.println("Enter the product to be searched:");
String p=s.nextLine();
boolean answer=sh.checkProductAvailability(p);
if(answer)
System.out.println("Product is available at "+sh.shopName+", "+sh.shopAddress+".");
else
System.out.println("Product is not available at "+sh.shopName+", "+sh.shopAddress+".");
}
}
