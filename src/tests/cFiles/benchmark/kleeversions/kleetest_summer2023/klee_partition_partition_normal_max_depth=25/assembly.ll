; ModuleID = '/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/partition_partition_.bc'
source_filename = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/partition_partition_.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [33 x i8] c"e31df0ddf5324bef9ba1a18b1a2dce77\00", align 1
@.str.1 = private unnamed_addr constant [33 x i8] c"02bccb40e027413a9b690bdc4740589a\00", align 1
@.str.2 = private unnamed_addr constant [33 x i8] c"97c45b37fda84cfcb1d0c69ad781e69c\00", align 1
@.str.3 = private unnamed_addr constant [50 x i8] c"/app/klee/runtime/Intrinsic/klee_div_zero_check.c\00", align 1
@.str.1.4 = private unnamed_addr constant [15 x i8] c"divide by zero\00", align 1
@.str.2.5 = private unnamed_addr constant [8 x i8] c"div.err\00", align 1

; Function Attrs: noinline nounwind uwtable
define void @swap(i32*, i32*) #0 !dbg !9 {
  %3 = alloca i32*, align 8
  %4 = alloca i32*, align 8
  %5 = alloca i32, align 4
  store i32* %0, i32** %3, align 8
  call void @llvm.dbg.declare(metadata i32** %3, metadata !15, metadata !DIExpression()), !dbg !16
  store i32* %1, i32** %4, align 8
  call void @llvm.dbg.declare(metadata i32** %4, metadata !17, metadata !DIExpression()), !dbg !18
  call void @llvm.dbg.declare(metadata i32* %5, metadata !19, metadata !DIExpression()), !dbg !20
  %6 = load i32*, i32** %3, align 8, !dbg !21
  %7 = load i32, i32* %6, align 4, !dbg !22
  store i32 %7, i32* %5, align 4, !dbg !20
  %8 = load i32*, i32** %4, align 8, !dbg !23
  %9 = load i32, i32* %8, align 4, !dbg !24
  %10 = load i32*, i32** %3, align 8, !dbg !25
  store i32 %9, i32* %10, align 4, !dbg !26
  %11 = load i32, i32* %5, align 4, !dbg !27
  %12 = load i32*, i32** %4, align 8, !dbg !28
  store i32 %11, i32* %12, align 4, !dbg !29
  ret void, !dbg !30
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline nounwind uwtable
define i32 @partition(i32*, i32, i32) #0 !dbg !31 {
  %4 = alloca i32*, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32* %0, i32** %4, align 8
  call void @llvm.dbg.declare(metadata i32** %4, metadata !34, metadata !DIExpression()), !dbg !35
  store i32 %1, i32* %5, align 4
  call void @llvm.dbg.declare(metadata i32* %5, metadata !36, metadata !DIExpression()), !dbg !37
  store i32 %2, i32* %6, align 4
  call void @llvm.dbg.declare(metadata i32* %6, metadata !38, metadata !DIExpression()), !dbg !39
  %9 = load i32*, i32** %4, align 8, !dbg !40
  %10 = load i32, i32* %5, align 4, !dbg !41
  %11 = call i32 @rand() #5, !dbg !42
  %12 = load i32, i32* %6, align 4, !dbg !43
  %13 = load i32, i32* %5, align 4, !dbg !44
  %14 = sub nsw i32 %12, %13, !dbg !45
  %15 = add nsw i32 %14, 1, !dbg !46
  %int_cast_to_i64 = zext i32 %15 to i64, !dbg !47
  call void @klee_div_zero_check(i64 %int_cast_to_i64), !dbg !47
  %16 = srem i32 %11, %15, !dbg !47, !klee.check.div !48
  %17 = add nsw i32 %10, %16, !dbg !49
  %18 = sext i32 %17 to i64, !dbg !40
  %19 = getelementptr inbounds i32, i32* %9, i64 %18, !dbg !40
  %20 = load i32*, i32** %4, align 8, !dbg !50
  %21 = load i32, i32* %6, align 4, !dbg !51
  %22 = sext i32 %21 to i64, !dbg !50
  %23 = getelementptr inbounds i32, i32* %20, i64 %22, !dbg !50
  call void @swap(i32* %19, i32* %23), !dbg !52
  call void @llvm.dbg.declare(metadata i32* %7, metadata !53, metadata !DIExpression()), !dbg !54
  %24 = load i32, i32* %5, align 4, !dbg !55
  %25 = sub nsw i32 %24, 1, !dbg !56
  store i32 %25, i32* %7, align 4, !dbg !54
  call void @llvm.dbg.declare(metadata i32* %8, metadata !57, metadata !DIExpression()), !dbg !59
  %26 = load i32, i32* %5, align 4, !dbg !60
  store i32 %26, i32* %8, align 4, !dbg !59
  br label %27, !dbg !61

; <label>:27:                                     ; preds = %53, %3
  %28 = load i32, i32* %8, align 4, !dbg !62
  %29 = load i32, i32* %6, align 4, !dbg !64
  %30 = icmp sle i32 %28, %29, !dbg !65
  br i1 %30, label %31, label %56, !dbg !66

; <label>:31:                                     ; preds = %27
  %32 = load i32*, i32** %4, align 8, !dbg !67
  %33 = load i32, i32* %8, align 4, !dbg !70
  %34 = sext i32 %33 to i64, !dbg !67
  %35 = getelementptr inbounds i32, i32* %32, i64 %34, !dbg !67
  %36 = load i32, i32* %35, align 4, !dbg !67
  %37 = load i32*, i32** %4, align 8, !dbg !71
  %38 = load i32, i32* %6, align 4, !dbg !72
  %39 = sext i32 %38 to i64, !dbg !71
  %40 = getelementptr inbounds i32, i32* %37, i64 %39, !dbg !71
  %41 = load i32, i32* %40, align 4, !dbg !71
  %42 = icmp sle i32 %36, %41, !dbg !73
  br i1 %42, label %43, label %53, !dbg !74

; <label>:43:                                     ; preds = %31
  %44 = load i32*, i32** %4, align 8, !dbg !75
  %45 = load i32, i32* %7, align 4, !dbg !77
  %46 = add nsw i32 %45, 1, !dbg !77
  store i32 %46, i32* %7, align 4, !dbg !77
  %47 = sext i32 %46 to i64, !dbg !75
  %48 = getelementptr inbounds i32, i32* %44, i64 %47, !dbg !75
  %49 = load i32*, i32** %4, align 8, !dbg !78
  %50 = load i32, i32* %8, align 4, !dbg !79
  %51 = sext i32 %50 to i64, !dbg !78
  %52 = getelementptr inbounds i32, i32* %49, i64 %51, !dbg !78
  call void @swap(i32* %48, i32* %52), !dbg !80
  br label %53, !dbg !81

; <label>:53:                                     ; preds = %31, %43
  %54 = load i32, i32* %8, align 4, !dbg !82
  %55 = add nsw i32 %54, 1, !dbg !82
  store i32 %55, i32* %8, align 4, !dbg !82
  br label %27, !dbg !83, !llvm.loop !84

; <label>:56:                                     ; preds = %27
  %57 = load i32, i32* %7, align 4, !dbg !86
  ret i32 %57, !dbg !87
}

; Function Attrs: nounwind
declare i32 @rand() #2

; Function Attrs: noinline nounwind uwtable
define i32 @main() #0 !dbg !88 {
  %1 = alloca i32, align 4
  %2 = alloca [1000 x i32], align 16
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata [1000 x i32]* %2, metadata !91, metadata !DIExpression()), !dbg !95
  %5 = bitcast [1000 x i32]* %2 to i8*, !dbg !96
  call void @klee_make_symbolic(i8* %5, i64 4000, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str, i32 0, i32 0)), !dbg !97
  call void @llvm.dbg.declare(metadata i32* %3, metadata !98, metadata !DIExpression()), !dbg !99
  %6 = bitcast i32* %3 to i8*, !dbg !100
  call void @klee_make_symbolic(i8* %6, i64 4, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str.1, i32 0, i32 0)), !dbg !101
  %7 = load i32, i32* %3, align 4, !dbg !102
  %8 = icmp slt i32 %7, -1, !dbg !104
  %9 = load i32, i32* %3, align 4, !dbg !105
  %10 = icmp sgt i32 %9, 1024, !dbg !106
  %or.cond = or i1 %8, %10, !dbg !107
  br i1 %or.cond, label %11, label %12, !dbg !107

; <label>:11:                                     ; preds = %0
  store i32 0, i32* %1, align 4, !dbg !108
  br label %24, !dbg !108

; <label>:12:                                     ; preds = %0
  call void @llvm.dbg.declare(metadata i32* %4, metadata !110, metadata !DIExpression()), !dbg !111
  %13 = bitcast i32* %4 to i8*, !dbg !112
  call void @klee_make_symbolic(i8* %13, i64 4, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str.2, i32 0, i32 0)), !dbg !113
  %14 = load i32, i32* %4, align 4, !dbg !114
  %15 = icmp slt i32 %14, -1, !dbg !116
  %16 = load i32, i32* %4, align 4, !dbg !117
  %17 = icmp sgt i32 %16, 1024, !dbg !118
  %or.cond3 = or i1 %15, %17, !dbg !119
  br i1 %or.cond3, label %18, label %19, !dbg !119

; <label>:18:                                     ; preds = %12
  store i32 0, i32* %1, align 4, !dbg !120
  br label %24, !dbg !120

; <label>:19:                                     ; preds = %12
  %20 = getelementptr inbounds [1000 x i32], [1000 x i32]* %2, i32 0, i32 0, !dbg !122
  %21 = load i32, i32* %3, align 4, !dbg !123
  %22 = load i32, i32* %4, align 4, !dbg !124
  %23 = call i32 @partition(i32* %20, i32 %21, i32 %22), !dbg !125
  store i32 %23, i32* %1, align 4, !dbg !126
  br label %24, !dbg !126

; <label>:24:                                     ; preds = %19, %18, %11
  %25 = load i32, i32* %1, align 4, !dbg !127
  ret i32 %25, !dbg !127
}

declare void @klee_make_symbolic(i8*, i64, i8*) #3

; Function Attrs: noinline nounwind uwtable
define void @klee_div_zero_check(i64) #0 !dbg !128 {
  %2 = alloca i64, align 8
  store i64 %0, i64* %2, align 8
  call void @llvm.dbg.declare(metadata i64* %2, metadata !132, metadata !DIExpression()), !dbg !133
  %3 = load i64, i64* %2, align 8, !dbg !134
  %4 = icmp eq i64 %3, 0, !dbg !136
  br i1 %4, label %5, label %6, !dbg !137

; <label>:5:                                      ; preds = %1
  call void @klee_report_error(i8* getelementptr inbounds ([50 x i8], [50 x i8]* @.str.3, i32 0, i32 0), i32 14, i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.str.1.4, i32 0, i32 0), i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.2.5, i32 0, i32 0)) #6, !dbg !138
  unreachable, !dbg !138

; <label>:6:                                      ; preds = %1
  ret void, !dbg !139
}

; Function Attrs: noreturn
declare void @klee_report_error(i8*, i32, i8*, i8*) #4

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noreturn "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nounwind }
attributes #6 = { noreturn }

!llvm.dbg.cu = !{!0, !3}
!llvm.module.flags = !{!5, !6, !7}
!llvm.ident = !{!8, !8}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1-10 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)
!1 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/partition_partition_.c", directory: "/app/code")
!2 = !{}
!3 = distinct !DICompileUnit(language: DW_LANG_C89, file: !4, producer: "clang version 6.0.1-10 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)
!4 = !DIFile(filename: "/app/klee/runtime/Intrinsic/klee_div_zero_check.c", directory: "/app/build/runtime/Intrinsic")
!5 = !{i32 2, !"Dwarf Version", i32 4}
!6 = !{i32 2, !"Debug Info Version", i32 3}
!7 = !{i32 1, !"wchar_size", i32 4}
!8 = !{!"clang version 6.0.1-10 (tags/RELEASE_601/final)"}
!9 = distinct !DISubprogram(name: "swap", scope: !10, file: !10, line: 4, type: !11, isLocal: false, isDefinition: true, scopeLine: 4, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!10 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/cFiles/partition.c", directory: "/app/code")
!11 = !DISubroutineType(types: !12)
!12 = !{null, !13, !13}
!13 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !14, size: 64)
!14 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!15 = !DILocalVariable(name: "a", arg: 1, scope: !9, file: !10, line: 4, type: !13)
!16 = !DILocation(line: 4, column: 16, scope: !9)
!17 = !DILocalVariable(name: "b", arg: 2, scope: !9, file: !10, line: 4, type: !13)
!18 = !DILocation(line: 4, column: 24, scope: !9)
!19 = !DILocalVariable(name: "c", scope: !9, file: !10, line: 5, type: !14)
!20 = !DILocation(line: 5, column: 7, scope: !9)
!21 = !DILocation(line: 5, column: 12, scope: !9)
!22 = !DILocation(line: 5, column: 11, scope: !9)
!23 = !DILocation(line: 6, column: 9, scope: !9)
!24 = !DILocation(line: 6, column: 8, scope: !9)
!25 = !DILocation(line: 6, column: 4, scope: !9)
!26 = !DILocation(line: 6, column: 6, scope: !9)
!27 = !DILocation(line: 7, column: 8, scope: !9)
!28 = !DILocation(line: 7, column: 4, scope: !9)
!29 = !DILocation(line: 7, column: 6, scope: !9)
!30 = !DILocation(line: 8, column: 1, scope: !9)
!31 = distinct !DISubprogram(name: "partition", scope: !10, file: !10, line: 10, type: !32, isLocal: false, isDefinition: true, scopeLine: 10, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!32 = !DISubroutineType(types: !33)
!33 = !{!14, !13, !14, !14}
!34 = !DILocalVariable(name: "A", arg: 1, scope: !31, file: !10, line: 10, type: !13)
!35 = !DILocation(line: 10, column: 19, scope: !31)
!36 = !DILocalVariable(name: "p", arg: 2, scope: !31, file: !10, line: 10, type: !14)
!37 = !DILocation(line: 10, column: 28, scope: !31)
!38 = !DILocalVariable(name: "q", arg: 3, scope: !31, file: !10, line: 10, type: !14)
!39 = !DILocation(line: 10, column: 35, scope: !31)
!40 = !DILocation(line: 11, column: 9, scope: !31)
!41 = !DILocation(line: 11, column: 11, scope: !31)
!42 = !DILocation(line: 11, column: 16, scope: !31)
!43 = !DILocation(line: 11, column: 26, scope: !31)
!44 = !DILocation(line: 11, column: 30, scope: !31)
!45 = !DILocation(line: 11, column: 28, scope: !31)
!46 = !DILocation(line: 11, column: 32, scope: !31)
!47 = !DILocation(line: 11, column: 23, scope: !31)
!48 = !{!"True"}
!49 = !DILocation(line: 11, column: 13, scope: !31)
!50 = !DILocation(line: 11, column: 41, scope: !31)
!51 = !DILocation(line: 11, column: 43, scope: !31)
!52 = !DILocation(line: 11, column: 3, scope: !31)
!53 = !DILocalVariable(name: "i", scope: !31, file: !10, line: 13, type: !14)
!54 = !DILocation(line: 13, column: 7, scope: !31)
!55 = !DILocation(line: 13, column: 11, scope: !31)
!56 = !DILocation(line: 13, column: 13, scope: !31)
!57 = !DILocalVariable(name: "j", scope: !58, file: !10, line: 14, type: !14)
!58 = distinct !DILexicalBlock(scope: !31, file: !10, line: 14, column: 3)
!59 = !DILocation(line: 14, column: 11, scope: !58)
!60 = !DILocation(line: 14, column: 15, scope: !58)
!61 = !DILocation(line: 14, column: 7, scope: !58)
!62 = !DILocation(line: 14, column: 18, scope: !63)
!63 = distinct !DILexicalBlock(scope: !58, file: !10, line: 14, column: 3)
!64 = !DILocation(line: 14, column: 23, scope: !63)
!65 = !DILocation(line: 14, column: 20, scope: !63)
!66 = !DILocation(line: 14, column: 3, scope: !58)
!67 = !DILocation(line: 15, column: 8, scope: !68)
!68 = distinct !DILexicalBlock(scope: !69, file: !10, line: 15, column: 8)
!69 = distinct !DILexicalBlock(scope: !63, file: !10, line: 14, column: 31)
!70 = !DILocation(line: 15, column: 10, scope: !68)
!71 = !DILocation(line: 15, column: 16, scope: !68)
!72 = !DILocation(line: 15, column: 18, scope: !68)
!73 = !DILocation(line: 15, column: 13, scope: !68)
!74 = !DILocation(line: 15, column: 8, scope: !69)
!75 = !DILocation(line: 16, column: 13, scope: !76)
!76 = distinct !DILexicalBlock(scope: !68, file: !10, line: 15, column: 22)
!77 = !DILocation(line: 16, column: 15, scope: !76)
!78 = !DILocation(line: 16, column: 22, scope: !76)
!79 = !DILocation(line: 16, column: 24, scope: !76)
!80 = !DILocation(line: 16, column: 7, scope: !76)
!81 = !DILocation(line: 17, column: 5, scope: !76)
!82 = !DILocation(line: 14, column: 27, scope: !63)
!83 = !DILocation(line: 14, column: 3, scope: !63)
!84 = distinct !{!84, !66, !85}
!85 = !DILocation(line: 18, column: 3, scope: !58)
!86 = !DILocation(line: 20, column: 10, scope: !31)
!87 = !DILocation(line: 20, column: 3, scope: !31)
!88 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 4, type: !89, isLocal: false, isDefinition: true, scopeLine: 4, isOptimized: false, unit: !0, variables: !2)
!89 = !DISubroutineType(types: !90)
!90 = !{!14}
!91 = !DILocalVariable(name: "A", scope: !88, file: !1, line: 6, type: !92)
!92 = !DICompositeType(tag: DW_TAG_array_type, baseType: !14, size: 32000, elements: !93)
!93 = !{!94}
!94 = !DISubrange(count: 1000)
!95 = !DILocation(line: 6, column: 6, scope: !88)
!96 = !DILocation(line: 7, column: 21, scope: !88)
!97 = !DILocation(line: 7, column: 2, scope: !88)
!98 = !DILocalVariable(name: "p", scope: !88, file: !1, line: 9, type: !14)
!99 = !DILocation(line: 9, column: 6, scope: !88)
!100 = !DILocation(line: 10, column: 21, scope: !88)
!101 = !DILocation(line: 10, column: 2, scope: !88)
!102 = !DILocation(line: 11, column: 7, scope: !103)
!103 = distinct !DILexicalBlock(scope: !88, file: !1, line: 11, column: 6)
!104 = !DILocation(line: 11, column: 8, scope: !103)
!105 = !DILocation(line: 11, column: 17, scope: !103)
!106 = !DILocation(line: 11, column: 18, scope: !103)
!107 = !DILocation(line: 11, column: 13, scope: !103)
!108 = !DILocation(line: 12, column: 4, scope: !109)
!109 = distinct !DILexicalBlock(scope: !103, file: !1, line: 11, column: 26)
!110 = !DILocalVariable(name: "q", scope: !88, file: !1, line: 14, type: !14)
!111 = !DILocation(line: 14, column: 6, scope: !88)
!112 = !DILocation(line: 15, column: 21, scope: !88)
!113 = !DILocation(line: 15, column: 2, scope: !88)
!114 = !DILocation(line: 16, column: 7, scope: !115)
!115 = distinct !DILexicalBlock(scope: !88, file: !1, line: 16, column: 6)
!116 = !DILocation(line: 16, column: 8, scope: !115)
!117 = !DILocation(line: 16, column: 17, scope: !115)
!118 = !DILocation(line: 16, column: 18, scope: !115)
!119 = !DILocation(line: 16, column: 13, scope: !115)
!120 = !DILocation(line: 17, column: 4, scope: !121)
!121 = distinct !DILexicalBlock(scope: !115, file: !1, line: 16, column: 26)
!122 = !DILocation(line: 18, column: 19, scope: !88)
!123 = !DILocation(line: 18, column: 22, scope: !88)
!124 = !DILocation(line: 18, column: 25, scope: !88)
!125 = !DILocation(line: 18, column: 9, scope: !88)
!126 = !DILocation(line: 18, column: 2, scope: !88)
!127 = !DILocation(line: 19, column: 1, scope: !88)
!128 = distinct !DISubprogram(name: "klee_div_zero_check", scope: !4, file: !4, line: 12, type: !129, isLocal: false, isDefinition: true, scopeLine: 12, flags: DIFlagPrototyped, isOptimized: false, unit: !3, variables: !2)
!129 = !DISubroutineType(types: !130)
!130 = !{null, !131}
!131 = !DIBasicType(name: "long long int", size: 64, encoding: DW_ATE_signed)
!132 = !DILocalVariable(name: "z", arg: 1, scope: !128, file: !4, line: 12, type: !131)
!133 = !DILocation(line: 12, column: 36, scope: !128)
!134 = !DILocation(line: 13, column: 7, scope: !135)
!135 = distinct !DILexicalBlock(scope: !128, file: !4, line: 13, column: 7)
!136 = !DILocation(line: 13, column: 9, scope: !135)
!137 = !DILocation(line: 13, column: 7, scope: !128)
!138 = !DILocation(line: 14, column: 5, scope: !135)
!139 = !DILocation(line: 15, column: 1, scope: !128)
