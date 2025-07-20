# health.py

This is a simple script that monitors URLs (configured in the data array in the code) and displays a nice report in the terminal

By default, the script looks only at the http status codes, but it can optionally compare an md5 hash of the contents of the page with one if you configure that in the data section. 

### Example URL Configuration

```
data = [
    ["Random"],
    ["chasta.in", "https://chasta.in", "40386eeefe7cc450fcc797bab8fba754"],
    ["google", "https://www.google.com"],
    ["aws", "https://www.aws.com"],
    ["duck", "https://www.duck.com"],
]
```

"Random" is a heading, it's just a nice way to group the URLs in the terminal when showing the report, it can be any descriptive string you want.

The other entries represent URLs to monitor. The first column is the name for reporting purposes, the second obviously is the URL you want to monitor, and the third (optional) is an md5 hash of the contents of the page which enables comparing the current contents of the page with a known good version of the contents.

If you want to compare the md5 hash but don't have it, just enter a fake value and save it, then run the code and the report will show you the current md5 hash which you can then just copy over the fake value.

