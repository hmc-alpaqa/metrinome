; ModuleID = '/app/code/tests/cFiles/benchmark/kleeversions/kleetest/digital-root-multiplicative-digital-root__mdr_.bc'
source_filename = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest/digital-root-multiplicative-digital-root__mdr_.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [33 x i8] c"0678b10bf16342d08809ceec57f9c8f1\00", align 1
@.str.1 = private unnamed_addr constant [33 x i8] c"b65a9c6dd14c4ca08ce7f6955dc56508\00", align 1
@.str.2 = private unnamed_addr constant [33 x i8] c"fd79f77ec4cf47868a48dff96655c5ac\00", align 1

; Function Attrs: nounwind uwtable
define void @_mdr(i32* nocapture, i32* nocapture, i64) local_unnamed_addr #0 !dbg !7 {
  %4 = load i32, i32* %1, align 4, !dbg !19, !tbaa !20
  br label %5

; <label>:5:                                      ; preds = %23, %3
  %6 = phi i32 [ %4, %3 ], [ %24, %23 ]
  %7 = phi i64 [ %2, %3 ], [ %26, %23 ]
  call void @llvm.dbg.value(metadata i32* %0, metadata !15, metadata !DIExpression()), !dbg !24
  call void @llvm.dbg.value(metadata i32* %1, metadata !16, metadata !DIExpression()), !dbg !25
  call void @llvm.dbg.value(metadata i64 %7, metadata !17, metadata !DIExpression()), !dbg !26
  %8 = icmp ne i64 %7, 0, !dbg !27
  call void @llvm.dbg.value(metadata i32 %10, metadata !18, metadata !DIExpression()), !dbg !28
  call void @llvm.dbg.value(metadata i64 %7, metadata !17, metadata !DIExpression()), !dbg !26
  %9 = icmp eq i64 %7, 0, !dbg !29
  %10 = zext i1 %8 to i32, !dbg !27
  br i1 %9, label %12, label %11, !dbg !29

; <label>:11:                                     ; preds = %5
  br label %14, !dbg !30

; <label>:12:                                     ; preds = %5
  %13 = add nsw i32 %6, 1, !dbg !19
  br label %27, !dbg !32

; <label>:14:                                     ; preds = %11, %14
  %15 = phi i32 [ %19, %14 ], [ %10, %11 ]
  %16 = phi i64 [ %20, %14 ], [ %7, %11 ]
  call void @llvm.dbg.value(metadata i64 %16, metadata !17, metadata !DIExpression()), !dbg !26
  call void @llvm.dbg.value(metadata i32 %15, metadata !18, metadata !DIExpression()), !dbg !28
  %17 = srem i64 %16, 10, !dbg !30
  %18 = trunc i64 %17 to i32, !dbg !33
  %19 = mul i32 %15, %18, !dbg !33
  %20 = sdiv i64 %16, 10, !dbg !34
  call void @llvm.dbg.value(metadata i32 %19, metadata !18, metadata !DIExpression()), !dbg !28
  call void @llvm.dbg.value(metadata i64 %20, metadata !17, metadata !DIExpression()), !dbg !26
  %21 = add i64 %16, 9, !dbg !29
  %22 = icmp ult i64 %21, 19, !dbg !29
  br i1 %22, label %23, label %14, !dbg !29, !llvm.loop !35

; <label>:23:                                     ; preds = %14
  %24 = add nsw i32 %6, 1, !dbg !19
  %25 = icmp sgt i32 %19, 9, !dbg !37
  %26 = sext i32 %19 to i64, !dbg !39
  br i1 %25, label %5, label %27, !dbg !32

; <label>:27:                                     ; preds = %23, %12
  %28 = phi i32 [ %13, %12 ], [ %24, %23 ]
  %29 = phi i32 [ %10, %12 ], [ %19, %23 ]
  store i32 %28, i32* %1, align 4, !dbg !19, !tbaa !20
  store i32 %29, i32* %0, align 4, !dbg !40, !tbaa !20
  ret void, !dbg !41
}

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.start.p0i8(i64, i8* nocapture) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.end.p0i8(i64, i8* nocapture) #1

; Function Attrs: nounwind uwtable
define i32 @main() local_unnamed_addr #0 !dbg !42 {
  %1 = alloca i32*, align 8
  %2 = alloca i32*, align 8
  %3 = alloca i64, align 8
  %4 = bitcast i32** %1 to i8*, !dbg !49
  call void @klee_make_symbolic(i8* nonnull %4, i64 8, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str, i64 0, i64 0)) #4, !dbg !50
  %5 = bitcast i32** %2 to i8*, !dbg !51
  call void @klee_make_symbolic(i8* nonnull %5, i64 8, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str.1, i64 0, i64 0)) #4, !dbg !52
  %6 = bitcast i64* %3 to i8*, !dbg !53
  call void @klee_make_symbolic(i8* nonnull %6, i64 8, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str.2, i64 0, i64 0)) #4, !dbg !54
  %7 = load i32*, i32** %1, align 8, !dbg !55, !tbaa !56
  call void @llvm.dbg.value(metadata i32* %7, metadata !46, metadata !DIExpression()), !dbg !58
  %8 = load i32*, i32** %2, align 8, !dbg !59, !tbaa !56
  call void @llvm.dbg.value(metadata i32* %8, metadata !47, metadata !DIExpression()), !dbg !60
  %9 = load i64, i64* %3, align 8, !dbg !61, !tbaa !62
  call void @llvm.dbg.value(metadata i64 %9, metadata !48, metadata !DIExpression()), !dbg !64
  call void @_mdr(i32* %7, i32* %8, i64 %9), !dbg !65
  ret i32 0, !dbg !66
}

declare void @klee_make_symbolic(i8*, i64, i8*) local_unnamed_addr #2

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.value(metadata, metadata, metadata) #3

attributes #0 = { nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readnone speculatable }
attributes #4 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1-10 (tags/RELEASE_601/final)", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)
!1 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest/digital-root-multiplicative-digital-root__mdr_.c", directory: "/app/code")
!2 = !{}
!3 = !{i32 2, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 6.0.1-10 (tags/RELEASE_601/final)"}
!7 = distinct !DISubprogram(name: "_mdr", scope: !8, file: !8, line: 7, type: !9, isLocal: false, isDefinition: true, scopeLine: 8, flags: DIFlagPrototyped, isOptimized: true, unit: !0, variables: !14)
!8 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/files/digital-root-multiplicative-digital-root.c", directory: "/app/code")
!9 = !DISubroutineType(types: !10)
!10 = !{null, !11, !11, !13}
!11 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !12, size: 64)
!12 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!13 = !DIBasicType(name: "long long int", size: 64, encoding: DW_ATE_signed)
!14 = !{!15, !16, !17, !18}
!15 = !DILocalVariable(name: "rmdr", arg: 1, scope: !7, file: !8, line: 7, type: !11)
!16 = !DILocalVariable(name: "rmp", arg: 2, scope: !7, file: !8, line: 7, type: !11)
!17 = !DILocalVariable(name: "n", arg: 3, scope: !7, file: !8, line: 7, type: !13)
!18 = !DILocalVariable(name: "r", scope: !7, file: !8, line: 10, type: !12)
!19 = !DILocation(line: 16, column: 11, scope: !7)
!20 = !{!21, !21, i64 0}
!21 = !{!"int", !22, i64 0}
!22 = !{!"omnipotent char", !23, i64 0}
!23 = !{!"Simple C/C++ TBAA"}
!24 = !DILocation(line: 7, column: 16, scope: !7)
!25 = !DILocation(line: 7, column: 27, scope: !7)
!26 = !DILocation(line: 7, column: 42, scope: !7)
!27 = !DILocation(line: 10, column: 13, scope: !7)
!28 = !DILocation(line: 10, column: 9, scope: !7)
!29 = !DILocation(line: 11, column: 5, scope: !7)
!30 = !DILocation(line: 12, column: 17, scope: !31)
!31 = distinct !DILexicalBlock(scope: !7, file: !8, line: 11, column: 15)
!32 = !DILocation(line: 17, column: 9, scope: !7)
!33 = !DILocation(line: 12, column: 11, scope: !31)
!34 = !DILocation(line: 13, column: 11, scope: !31)
!35 = distinct !{!35, !29, !36}
!36 = !DILocation(line: 14, column: 5, scope: !7)
!37 = !DILocation(line: 17, column: 11, scope: !38)
!38 = distinct !DILexicalBlock(scope: !7, file: !8, line: 17, column: 9)
!39 = !DILocation(line: 18, column: 25, scope: !38)
!40 = !DILocation(line: 20, column: 15, scope: !38)
!41 = !DILocation(line: 21, column: 1, scope: !7)
!42 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 4, type: !43, isLocal: false, isDefinition: true, scopeLine: 4, isOptimized: true, unit: !0, variables: !45)
!43 = !DISubroutineType(types: !44)
!44 = !{!12}
!45 = !{!46, !47, !48}
!46 = !DILocalVariable(name: "rmdr", scope: !42, file: !1, line: 6, type: !11)
!47 = !DILocalVariable(name: "rmp", scope: !42, file: !1, line: 9, type: !11)
!48 = !DILocalVariable(name: "n", scope: !42, file: !1, line: 12, type: !13)
!49 = !DILocation(line: 6, column: 2, scope: !42)
!50 = !DILocation(line: 7, column: 2, scope: !42)
!51 = !DILocation(line: 9, column: 2, scope: !42)
!52 = !DILocation(line: 10, column: 2, scope: !42)
!53 = !DILocation(line: 12, column: 2, scope: !42)
!54 = !DILocation(line: 13, column: 2, scope: !42)
!55 = !DILocation(line: 14, column: 7, scope: !42)
!56 = !{!57, !57, i64 0}
!57 = !{!"any pointer", !22, i64 0}
!58 = !DILocation(line: 6, column: 7, scope: !42)
!59 = !DILocation(line: 14, column: 13, scope: !42)
!60 = !DILocation(line: 9, column: 7, scope: !42)
!61 = !DILocation(line: 14, column: 18, scope: !42)
!62 = !{!63, !63, i64 0}
!63 = !{!"long long", !22, i64 0}
!64 = !DILocation(line: 12, column: 12, scope: !42)
!65 = !DILocation(line: 14, column: 2, scope: !42)
!66 = !DILocation(line: 15, column: 2, scope: !42)
