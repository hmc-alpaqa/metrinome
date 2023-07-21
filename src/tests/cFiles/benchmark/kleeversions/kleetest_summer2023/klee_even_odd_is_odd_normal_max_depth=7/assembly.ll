; ModuleID = '/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/even_odd_is_odd_.bc'
source_filename = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/even_odd_is_odd_.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [33 x i8] c"b8835ef609ea403c92de3f4e0766d96f\00", align 1

; Function Attrs: noinline nounwind uwtable
define i32 @is_even(i32) #0 !dbg !7 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !12, metadata !DIExpression()), !dbg !13
  %4 = load i32, i32* %3, align 4, !dbg !14
  %5 = icmp eq i32 %4, 0, !dbg !16
  br i1 %5, label %6, label %7, !dbg !17

; <label>:6:                                      ; preds = %1
  store i32 1, i32* %2, align 4, !dbg !18
  br label %11, !dbg !18

; <label>:7:                                      ; preds = %1
  %8 = load i32, i32* %3, align 4, !dbg !20
  %9 = sub nsw i32 %8, 1, !dbg !22
  %10 = call i32 @is_odd(i32 %9), !dbg !23
  store i32 %10, i32* %2, align 4, !dbg !24
  br label %11, !dbg !24

; <label>:11:                                     ; preds = %7, %6
  %12 = load i32, i32* %2, align 4, !dbg !25
  ret i32 %12, !dbg !25
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline nounwind uwtable
define i32 @is_odd(i32) #0 !dbg !26 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !27, metadata !DIExpression()), !dbg !28
  %4 = load i32, i32* %3, align 4, !dbg !29
  %5 = icmp eq i32 %4, 0, !dbg !31
  br i1 %5, label %6, label %7, !dbg !32

; <label>:6:                                      ; preds = %1
  store i32 0, i32* %2, align 4, !dbg !33
  br label %11, !dbg !33

; <label>:7:                                      ; preds = %1
  %8 = load i32, i32* %3, align 4, !dbg !35
  %9 = sub nsw i32 %8, 1, !dbg !37
  %10 = call i32 @is_even(i32 %9), !dbg !38
  store i32 %10, i32* %2, align 4, !dbg !39
  br label %11, !dbg !39

; <label>:11:                                     ; preds = %7, %6
  %12 = load i32, i32* %2, align 4, !dbg !40
  ret i32 %12, !dbg !40
}

; Function Attrs: noinline nounwind uwtable
define i32 @main() #0 !dbg !41 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata i32* %2, metadata !44, metadata !DIExpression()), !dbg !45
  %3 = bitcast i32* %2 to i8*, !dbg !46
  call void @klee_make_symbolic(i8* %3, i64 4, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str, i32 0, i32 0)), !dbg !47
  %4 = load i32, i32* %2, align 4, !dbg !48
  %5 = icmp slt i32 %4, -1, !dbg !50
  %6 = load i32, i32* %2, align 4, !dbg !51
  %7 = icmp sgt i32 %6, 1024, !dbg !52
  %or.cond = or i1 %5, %7, !dbg !53
  br i1 %or.cond, label %8, label %9, !dbg !53

; <label>:8:                                      ; preds = %0
  store i32 0, i32* %1, align 4, !dbg !54
  br label %12, !dbg !54

; <label>:9:                                      ; preds = %0
  %10 = load i32, i32* %2, align 4, !dbg !56
  %11 = call i32 @is_odd(i32 %10), !dbg !57
  store i32 %11, i32* %1, align 4, !dbg !58
  br label %12, !dbg !58

; <label>:12:                                     ; preds = %9, %8
  %13 = load i32, i32* %1, align 4, !dbg !59
  ret i32 %13, !dbg !59
}

declare void @klee_make_symbolic(i8*, i64, i8*) #2

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1-10 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)
!1 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/even_odd_is_odd_.c", directory: "/app/code")
!2 = !{}
!3 = !{i32 2, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 6.0.1-10 (tags/RELEASE_601/final)"}
!7 = distinct !DISubprogram(name: "is_even", scope: !8, file: !8, line: 7, type: !9, isLocal: false, isDefinition: true, scopeLine: 8, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!8 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/cFiles/even_odd.c", directory: "/app/code")
!9 = !DISubroutineType(types: !10)
!10 = !{!11, !11}
!11 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!12 = !DILocalVariable(name: "n", arg: 1, scope: !7, file: !8, line: 7, type: !11)
!13 = !DILocation(line: 7, column: 17, scope: !7)
!14 = !DILocation(line: 9, column: 9, scope: !15)
!15 = distinct !DILexicalBlock(scope: !7, file: !8, line: 9, column: 9)
!16 = !DILocation(line: 9, column: 11, scope: !15)
!17 = !DILocation(line: 9, column: 9, scope: !7)
!18 = !DILocation(line: 11, column: 9, scope: !19)
!19 = distinct !DILexicalBlock(scope: !15, file: !8, line: 10, column: 5)
!20 = !DILocation(line: 15, column: 23, scope: !21)
!21 = distinct !DILexicalBlock(scope: !15, file: !8, line: 14, column: 5)
!22 = !DILocation(line: 15, column: 25, scope: !21)
!23 = !DILocation(line: 15, column: 16, scope: !21)
!24 = !DILocation(line: 15, column: 9, scope: !21)
!25 = !DILocation(line: 17, column: 1, scope: !7)
!26 = distinct !DISubprogram(name: "is_odd", scope: !8, file: !8, line: 19, type: !9, isLocal: false, isDefinition: true, scopeLine: 20, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!27 = !DILocalVariable(name: "n", arg: 1, scope: !26, file: !8, line: 19, type: !11)
!28 = !DILocation(line: 19, column: 16, scope: !26)
!29 = !DILocation(line: 21, column: 9, scope: !30)
!30 = distinct !DILexicalBlock(scope: !26, file: !8, line: 21, column: 9)
!31 = !DILocation(line: 21, column: 11, scope: !30)
!32 = !DILocation(line: 21, column: 9, scope: !26)
!33 = !DILocation(line: 23, column: 9, scope: !34)
!34 = distinct !DILexicalBlock(scope: !30, file: !8, line: 22, column: 5)
!35 = !DILocation(line: 27, column: 24, scope: !36)
!36 = distinct !DILexicalBlock(scope: !30, file: !8, line: 26, column: 5)
!37 = !DILocation(line: 27, column: 26, scope: !36)
!38 = !DILocation(line: 27, column: 16, scope: !36)
!39 = !DILocation(line: 27, column: 9, scope: !36)
!40 = !DILocation(line: 29, column: 1, scope: !26)
!41 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 4, type: !42, isLocal: false, isDefinition: true, scopeLine: 4, isOptimized: false, unit: !0, variables: !2)
!42 = !DISubroutineType(types: !43)
!43 = !{!11}
!44 = !DILocalVariable(name: "n", scope: !41, file: !1, line: 6, type: !11)
!45 = !DILocation(line: 6, column: 6, scope: !41)
!46 = !DILocation(line: 7, column: 21, scope: !41)
!47 = !DILocation(line: 7, column: 2, scope: !41)
!48 = !DILocation(line: 8, column: 7, scope: !49)
!49 = distinct !DILexicalBlock(scope: !41, file: !1, line: 8, column: 6)
!50 = !DILocation(line: 8, column: 8, scope: !49)
!51 = !DILocation(line: 8, column: 17, scope: !49)
!52 = !DILocation(line: 8, column: 18, scope: !49)
!53 = !DILocation(line: 8, column: 13, scope: !49)
!54 = !DILocation(line: 9, column: 4, scope: !55)
!55 = distinct !DILexicalBlock(scope: !49, file: !1, line: 8, column: 26)
!56 = !DILocation(line: 10, column: 16, scope: !41)
!57 = !DILocation(line: 10, column: 9, scope: !41)
!58 = !DILocation(line: 10, column: 2, scope: !41)
!59 = !DILocation(line: 11, column: 1, scope: !41)
