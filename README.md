# Drawio-Sub-Workflow-Highlighter

A sub-workflow highlighter script for drawio

## Example

The config file should use the same filename with the .drawio file. 
And they totally should under the same folder, such as this:

```
folder_name
 |
 +-- wf_highlighter.py
 |
 +-- test_doc.drawio
 |
 +-- test_doc.json
```

Here is a config file format example:

```json
{
  "workflow 1": [
    "Test 1",
    "Test 2",
    "Test 3",
    "Test 4",
    "Test 5",
    "Test 6",
    "Test 7"
  ],
  "workflow 2": [
    "Test 8",
    "Test 9",
    "Test 10",
    "Test 7",
    "Test 4"
  ]
}
```

Then, run the python script in the terminal:

```
python3 wf_highlighter.py test_doc
```

Before:

![](Pics/Before_0.jpg)

After:

![](Pics/After_0.jpg)

![](Pics/After_1.jpg)
