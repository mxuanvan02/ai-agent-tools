# Hands-on practice slides: real screenshots, annotation, legibility

Rules distilled from a classroom deck programme where the owner rejected decks
twice for the same two reasons. They apply to EVERY lesson that contains a
practice/hands-on segment — not just a representative slide or one lesson in a
multi-lesson deck.

## Rule 1 — Practice slides must show the real operation

Every practice step must carry all three components:

1. **Real screenshot** of the actual software/interface learners will use.
   Text-only descriptions or decorative icons do not count. If no real
   screenshot exists yet, report the gap explicitly instead of shipping a
   text description.
2. **Annotation**: each screenshot carries numbered red boxes plus a short
   label that points at exactly one visible location ("click the button in the
   top-right corner").
3. **Numbered steps** on the slide matching the annotated numbers.

Machine-checkable gate: for every slide whose role is "practice", count
non-logo `<image>` elements (or PPTX pictures). A practice slide with zero
images is a FAIL. List every failing slide; never let one pictured slide
stand in for the whole set.

## Rule 2 — Balanced layout, large legible text

- Body text floor: ≥ 18px on a 1280×720 canvas (≈ 13.5pt projected). Label
  text inside coloured callout blocks is body text — builders often default it
  smaller; set it explicitly.
- No dead white band larger than ~1/3 of the slide. If vision review reports
  a bottom gap, fill it with a real content block or enlarge the image — do
  not stretch shapes.
- Verify by eye on rendered images BEFORE reporting done; geometry gates
  alone do not catch balance problems.

## Screenshot → annotation workflow (proven)

1. **Capture real state.** Drive a real browser (search query typed, real
   result page) or a real desktop app window (e.g. a text editor opening the
   actual learner deliverable file). Record element coordinates from the DOM
   (`getBoundingClientRect`) or measure ink bounding boxes in the PNG — never
   eyeball annotation boxes.
2. **Annotate with PIL.** Red boxes from measured coordinates; numbered
   labels placed in a measured-empty column (count dark pixels per region to
   prove it is blank); thin connector lines from box to label.
3. **Vision-review the annotated image and iterate.** Typical failures, all
   caught by review rounds: labels overlapping content text, number badges
   covering the first characters of a line, adjacent boxes whose padding sums
   into a red line striking through text, boxes cutting off the tail of a
   long URL.
4. **Crop dead regions.** Screenshots often carry empty browser chrome or an
   editor window two-thirds blank. Measure the ink extent, crop to it, and
   update the declared pixel dimensions in the slide spec so the aspect ratio
   stays correct. Cropping is also what makes in-image text large enough to
   read when projected.

## Renderer artifacts

Some PPTX screenshot tools render inherited master/layout placeholders that
the actual slides never use (e.g. a stray date or duplicate page number at
the bottom). Prove it before "fixing" the deck: check the slide XML for
inherited placeholders (`<p:ph`) and grep the slide parts for the artifact
string. Zero hits means renderer artifact — document it and move on.
