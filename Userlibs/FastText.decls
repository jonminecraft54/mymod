; FastText.dll declarations -- DISABLED ON PURPOSE.
;
; On this compiler (BlitzPRO Legacy v2.100) a userlib does NOT shadow a built-in
; command: Text/SetFont/StringWidth/StringHeight/FontWidth/FontHeight all keep
; resolving to the built-ins, while LoadFont (8 args) resolves to FastText.
; That mix would hand a FastText font handle to the built-in SetFont/Text and
; crash at runtime, so these declarations are left commented out.
;
; The parameter counts below were read from the stdcall `ret N` of each export
; in FastText.dll and are believed correct, should a compiler that does override
; built-ins ever be used.
;
;.lib "FastText.dll"
;
;LoadFont%(name$,height%,bold%,italic%,underline%,angle#,smooth%,encoding%):"LoadFont_"
;FreeFont(font%):"FreeFont_"
;SetFont(font%):"SetFont_"
;Text(x%,y%,txt$,centerx%,centery%,encoding%):"Text_"
;TextRect(x%,y%,width%,height%,txt$,formatting%,encoding%):"TextRect_"
;TextBackground(red%,green%,blue%):"TextBackground_"
;StringWidth%(txt$,encoding%):"StringWidth_"
;StringHeight%(txt$,encoding%):"StringHeight_"
;FontWidth%():"FontWidth_"
;FontHeight%():"FontHeight_"
