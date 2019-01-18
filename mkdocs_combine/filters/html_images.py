import re


class ImageFilter(object):
    def run(self, lines):
        ret = []
        for line in lines:
            done = {}
            while True:
                src = ""
                alt = ""
                title = ""
                width = ""
                height = ""
                width_height = ""
                matchImg = re.search(r"<img ([^>]*)>([^<]*</img>)?", line)

                # image in html style?
                if matchImg:
                    if matchImg.group(0) in done:
                        break
                    allInfoElems = matchImg.group(1)
                    srcMatch = re.search(r"src=\"([^>\"]*)\"", allInfoElems)
                    if srcMatch:
                        src = srcMatch.group(1).replace("/./", "/").replace("/../", "/")
                    altMatch = re.search(r"alt=\"([^>\"]*)\"", allInfoElems)
                    if altMatch:
                        if altMatch.group(1) & altMatch.group(1) != "":
                            alt = altMatch.group(1)
                    titleMatch = re.search(r"title=\"([^>\"]*)\"", allInfoElems)
                    if titleMatch:
                        title = ' "' + titleMatch.group(1) + '"'
                    widthMatch = re.search(r"width=\"([^>\"]*)\"", allInfoElems)
                    if widthMatch:
                        width = "width=" + widthMatch.group(1) + "px "
                    heightMatch = re.search(r"height=\"([^>\"]*)\"", allInfoElems)
                    if heightMatch:
                        height = "height=" + heightMatch.group(1) + "px "
                    if width != "" or height != "":
                        width_height = "{ " + width + height + "}"
                else:
                    break
                line = re.sub(
                    r"<img [^>]*>([^<]*</img>)?",
                    "![%s](%s%s)%s" % (alt, src, title, width_height),
                    line,
                )
                done[matchImg.group(0)] = True
            ret.append(line)
        return ret
