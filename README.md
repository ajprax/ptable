# ptable
Python utility for formatting human readable tables

## Examples
```python
ptable(("one", "two", "three"), ("short", "medium but still pretty short", "really long " * 100))
```
returns
```
| one   | two                           | three                                                                                                                                                        |
| ----- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| short | medium but still pretty short | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long really long really long really long really long  |
|       |                               | really long really long really long really long really long really long really long really long really long                                                  |
```

```python
ptable(("one", "two", "three"), ("short", "medium but still pretty short", "really long " * 10), max_width=30)
```
returns
```
| one   | two    | three     |
| ----- | ------ | --------- |
| short | medium | really    |
|       | but    | long      |
|       | still  | really    |
|       | pretty | long      |
|       | short  | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
|       |        | really    |
|       |        | long      |
```