filename = "vlab_cs_ucsb_test_ShimpleExample_test3_0_basic.dot";

Get["bigO.m"];
Get["pathComplexity.m"];
G = Import[filename];
pc = pathComplexity[G];
