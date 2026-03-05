# SimDoc PDF Inspection

This document exercises all block types for PDF inspection.

## Contents

- [Headings](#headings)
  - [Headings](#headings-1)
    - [Headings](#headings-2)
- [Paragraphs](#paragraphs)
- [Lists](#lists)
  - [Unordered](#unordered)
  - [Ordered](#ordered)
- [Code Blocks](#code-blocks)
  - [Fence Escalation](#fence-escalation)
  - [Python Example](#python-example)
- [Tables](#tables)
  - [Escaping + Alignment](#escaping-alignment)
  - [Simple Table](#simple-table)
- [Horizontal Rule](#horizontal-rule)

## Headings

### Headings

#### Headings

##### Heading Level 5 (Not in TOC by default)

---

## Paragraphs

Paragraphs preserve
internal newlines.

Inline styling: **bold**, *italics*, ***both***.

---

## Lists

### Unordered

- alpha
  - beta
  - gamma
- delta

### Ordered

1. one
  1. two
  1. three
1. four

---

## Code Blocks

### Fence Escalation

````bash
line1
```
line2
````

### Python Example

```python
def main():
    print("Hello World!")
```

---

## Tables

### Escaping + Alignment

| a | b |
| --- | ---: |
| 1<br>2 | x\|y |
|  | ok |

### Simple Table

| a | b |
| --- | --- |
| 1 | 2 |
| 3 | 4 |

---

## Horizontal Rule

---
