; ModuleID = '/app/code/tests/cFiles/benchmark/kleeversions/kleetest/hailstone-sequence-2_hailstone_.bc'
source_filename = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest/hailstone-sequence-2_hailstone_.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@cache = local_unnamed_addr global [10000000 x i64] zeroinitializer, align 16, !dbg !0
@.str = private unnamed_addr constant [33 x i8] c"652b2a162fdc487f9f42fe9a342fa119\00", align 1

; Function Attrs: nounwind uwtable
define i64 @hailstone(i64) local_unnamed_addr #0 !dbg !16 {
  call void @llvm.dbg.value(metadata i64 %0, metadata !20, metadata !DIExpression()), !dbg !23
  %2 = icmp eq i64 %0, 1, !dbg !24
  br i1 %2, label %24, label %3, !dbg !26

; <label>:3:                                      ; preds = %1
  %4 = icmp ult i64 %0, 10000000, !dbg !27
  br i1 %4, label %5, label %9, !dbg !29

; <label>:5:                                      ; preds = %3
  %6 = getelementptr inbounds [10000000 x i64], [10000000 x i64]* @cache, i64 0, i64 %0, !dbg !30
  %7 = load i64, i64* %6, align 8, !dbg !30, !tbaa !31
  %8 = icmp eq i64 %7, 0, !dbg !30
  br i1 %8, label %9, label %24, !dbg !35

; <label>:9:                                      ; preds = %5, %3
  %10 = and i64 %0, 1, !dbg !36
  %11 = icmp eq i64 %10, 0, !dbg !36
  %12 = mul i64 %0, 3, !dbg !37
  %13 = add i64 %12, 1, !dbg !38
  %14 = lshr i64 %0, 1, !dbg !39
  %15 = select i1 %11, i64 %14, i64 %13, !dbg !40
  %16 = tail call i64 @hailstone(i64 %15), !dbg !41
  %17 = trunc i64 %16 to i32, !dbg !42
  %18 = add i32 %17, 1, !dbg !42
  call void @llvm.dbg.value(metadata i32 %18, metadata !21, metadata !DIExpression()), !dbg !43
  br i1 %4, label %19, label %22, !dbg !44

; <label>:19:                                     ; preds = %9
  %20 = sext i32 %18 to i64, !dbg !45
  %21 = getelementptr inbounds [10000000 x i64], [10000000 x i64]* @cache, i64 0, i64 %0, !dbg !47
  store i64 %20, i64* %21, align 8, !dbg !48, !tbaa !31
  br label %22, !dbg !47

; <label>:22:                                     ; preds = %19, %9
  %23 = sext i32 %18 to i64, !dbg !49
  br label %24, !dbg !50

; <label>:24:                                     ; preds = %5, %1, %22
  %25 = phi i64 [ %23, %22 ], [ 1, %1 ], [ %7, %5 ]
  ret i64 %25, !dbg !51
}

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.start.p0i8(i64, i8* nocapture) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.end.p0i8(i64, i8* nocapture) #1

; Function Attrs: nounwind uwtable
define i32 @main() local_unnamed_addr #0 !dbg !52 {
  %1 = alloca i64, align 8
  %2 = bitcast i64* %1 to i8*, !dbg !57
  call void @klee_make_symbolic(i8* nonnull %2, i64 8, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str, i64 0, i64 0)) #4, !dbg !58
  %3 = load i64, i64* %1, align 8, !dbg !59, !tbaa !31
  call void @llvm.dbg.value(metadata i64 %3, metadata !56, metadata !DIExpression()), !dbg !60
  %4 = call i64 @hailstone(i64 %3), !dbg !61
  %5 = trunc i64 %4 to i32, !dbg !61
  ret i32 %5, !dbg !62
}

declare void @klee_make_symbolic(i8*, i64, i8*) local_unnamed_addr #2

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.value(metadata, metadata, metadata) #3

attributes #0 = { nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readnone speculatable }
attributes #4 = { nounwind }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!12, !13, !14}
!llvm.ident = !{!15}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "cache", scope: !2, file: !6, line: 7, type: !7, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 6.0.1-10 (tags/RELEASE_601/final)", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5)
!3 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest/hailstone-sequence-2_hailstone_.c", directory: "/app/code/klee")
!4 = !{}
!5 = !{!0}
!6 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/files/hailstone-sequence-2.c", directory: "/app/code/klee")
!7 = !DICompositeType(tag: DW_TAG_array_type, baseType: !8, size: 640000000, elements: !10)
!8 = !DIDerivedType(tag: DW_TAG_typedef, name: "ulong", file: !6, line: 6, baseType: !9)
!9 = !DIBasicType(name: "long unsigned int", size: 64, encoding: DW_ATE_unsigned)
!10 = !{!11}
!11 = !DISubrange(count: 10000000)
!12 = !{i32 2, !"Dwarf Version", i32 4}
!13 = !{i32 2, !"Debug Info Version", i32 3}
!14 = !{i32 1, !"wchar_size", i32 4}
!15 = !{!"clang version 6.0.1-10 (tags/RELEASE_601/final)"}
!16 = distinct !DISubprogram(name: "hailstone", scope: !6, file: !6, line: 9, type: !17, isLocal: false, isDefinition: true, scopeLine: 10, flags: DIFlagPrototyped, isOptimized: true, unit: !2, variables: !19)
!17 = !DISubroutineType(types: !18)
!18 = !{!8, !8}
!19 = !{!20, !21}
!20 = !DILocalVariable(name: "n", arg: 1, scope: !16, file: !6, line: 9, type: !8)
!21 = !DILocalVariable(name: "x", scope: !16, file: !6, line: 11, type: !22)
!22 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!23 = !DILocation(line: 9, column: 23, scope: !16)
!24 = !DILocation(line: 12, column: 8, scope: !25)
!25 = distinct !DILexicalBlock(scope: !16, file: !6, line: 12, column: 6)
!26 = !DILocation(line: 12, column: 6, scope: !16)
!27 = !DILocation(line: 13, column: 8, scope: !28)
!28 = distinct !DILexicalBlock(scope: !16, file: !6, line: 13, column: 6)
!29 = !DILocation(line: 13, column: 13, scope: !28)
!30 = !DILocation(line: 13, column: 16, scope: !28)
!31 = !{!32, !32, i64 0}
!32 = !{!"long", !33, i64 0}
!33 = !{!"omnipotent char", !34, i64 0}
!34 = !{!"Simple C/C++ TBAA"}
!35 = !DILocation(line: 13, column: 6, scope: !16)
!36 = !DILocation(line: 15, column: 23, scope: !16)
!37 = !DILocation(line: 15, column: 32, scope: !16)
!38 = !DILocation(line: 15, column: 36, scope: !16)
!39 = !DILocation(line: 15, column: 44, scope: !16)
!40 = !DILocation(line: 15, column: 20, scope: !16)
!41 = !DILocation(line: 15, column: 10, scope: !16)
!42 = !DILocation(line: 15, column: 6, scope: !16)
!43 = !DILocation(line: 11, column: 6, scope: !16)
!44 = !DILocation(line: 16, column: 6, scope: !16)
!45 = !DILocation(line: 16, column: 25, scope: !46)
!46 = distinct !DILexicalBlock(scope: !16, file: !6, line: 16, column: 6)
!47 = !DILocation(line: 16, column: 14, scope: !46)
!48 = !DILocation(line: 16, column: 23, scope: !46)
!49 = !DILocation(line: 17, column: 9, scope: !16)
!50 = !DILocation(line: 17, column: 2, scope: !16)
!51 = !DILocation(line: 18, column: 1, scope: !16)
!52 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 4, type: !53, isLocal: false, isDefinition: true, scopeLine: 4, isOptimized: true, unit: !2, variables: !55)
!53 = !DISubroutineType(types: !54)
!54 = !{!22}
!55 = !{!56}
!56 = !DILocalVariable(name: "n", scope: !52, file: !3, line: 6, type: !8)
!57 = !DILocation(line: 6, column: 2, scope: !52)
!58 = !DILocation(line: 7, column: 2, scope: !52)
!59 = !DILocation(line: 8, column: 19, scope: !52)
!60 = !DILocation(line: 6, column: 8, scope: !52)
!61 = !DILocation(line: 8, column: 9, scope: !52)
!62 = !DILocation(line: 8, column: 2, scope: !52)
