# ptable
Python utility for formatting human readable tables
## Examples
### Smart wrapping wraps columns with long values first
`max_width` constrains the entire table (including margins). default is 200
```python
print(ptable(
    ("one", "two", "three"),
    ("short", "medium but still pretty short", " ".join(["really long"] * 20)),
    max_width=105))
```
```
| one   | two                           | three                                                       |
|:----- |:----------------------------- |:----------------------------------------------------------- |
| short | medium but still pretty short | really long really long really long really long really long |
|       |                               | really long really long really long really long really long |
|       |                               | really long really long really long really long really long |
|       |                               | really long really long really long really long really long |
```
### Justification by column
```python
print(ptable(
    ("one", "two", "three"),
    ("short", "medium but still pretty short", " ".join(["really long"] * 5)),
    max_width=30,
    justification=(ljust, cjust, rjust)))
```
```
| one   |  two   |  three |
|:----- |:------:| ------:|
| short | medium | really |
|       |  but   |   long |
|       | still  | really |
|       | pretty |   long |
|       | short  | really |
|       |        |   long |
|       |        | really |
|       |        |   long |
|       |        | really |
|       |        |   long |
```
### Custom formatter by data type
```python
import random
print(ptable(
    ("one", "two", "three"),
    *[[random.random(), random.randint(0, 1000), "abc"] for _ in range(3)],
    str_by_type={int: fmt("int: {}"), float: fmt("{:.4f}"), str: fmt("'{}'")}))
```
```
| one    | two      | three |
|:------ |:-------- |:----- |
| 0.3708 | int: 474 | 'abc' |
| 0.3068 | int: 185 | 'abc' |
| 0.9272 | int: 418 | 'abc' |
```
`fmt` is a provided helper for turning a format string into a function, but any function (`any => str`) is acceptable