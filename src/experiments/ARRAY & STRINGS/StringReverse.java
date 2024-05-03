import java.util.Scanner;
public class StringReverse {

public static void main(String[] args)
{
	String s="    I LOVE JAVA,   THE COFFEE     ";
		int i=s.length()-1;
		String ans="";
		while(i>=0) {
			while(i>=0 && s.charAt(i)==' ' ) i--;
			int j=i;
			if(i<0) break;
			while(i>=0 && s.charAt(i)!=' ')i--;
			if(ans.isEmpty())
			ans=ans.concat(s.substring(i+1,j+1));		//j+1 th character is not included
			else
				ans=ans.concat(" "+s.substring(i+1,j+1));
		}
		System.out.println(ans);
}
}
