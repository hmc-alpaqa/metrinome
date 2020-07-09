#include <graphics.h>
#include <conio.h>
int main()
{
    int gd = DETECT, gm;
   
    initgraph(&gd, &gm,"C:\\TC\\BGI");
   
    outtextxy(10, 20, "Graphics programming is fun!");
   
    circle(200, 200, 50);
   
    setcolor(BLUE);
   
    line(350, 250, 450, 50);
   
    getch();
    closegraph( );
    return 0;
}