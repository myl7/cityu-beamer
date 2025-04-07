## Task
Convert the provided document (document.md) into a professional LaTeX Beamer presentation.

## Content Requirements
- **Preserve all content**: DO NOT alter the text of the original document. DO NOT omit any details or information. DO NOT simplify important details.
- **Improved editing allowed**: You may edit for readability and visual purposes:
  - Proofread for grammatical errors
  - Break complex sentences into simpler ones
  - Simplify tedious expressions while preserving meaning
  - Improve clarity, conciseness, and readability
- **No Chinese Characters**: All text should be in English.

## Formatting Guidelines
- **Key points**: Use **bold text** for key points
- **Examples**: Place examples in visual decoration boxes
- **Content balancing**: 
  - Maximum 8 lines of text per frame
  - Maximum 2 lines of captions per image
  - One image per frame
  - One large table per frame
- **Visual elements**:
  - For image links in the document, reference them sequentially as images/image1.png, images/image2.png, etc.
  - Use \alert{} to highlight text marked as ::key point:: in the document

## Presentation Features
- **Citations**: Use footnotes in MLA style, e.g., \emph{Short Name, Brief Title or Author}\footnote{Wang, Zefeng, et al. "The art of automatic beamer." arXiv (2024).}
- **Animation**: Use \pause on pages with:
  - Two or more content groups
  - More than 6 lines of text

## Technical Details
- **Output filename**: main.tex
- **Template**: Use and follow the template located at template/slide.tex