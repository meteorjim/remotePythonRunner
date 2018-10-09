function absoluteXPath(element) {
    var comp, comps = [];
    var parent = null;
    var xpath = '';
    var getPos = function (element) {
        var position = 1,
            curNode;
        if (element.nodeType == Node.ATTRIBUTE_NODE) {
            return null;
        }
        for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {
            if (curNode.nodeName == element.nodeName) {
                ++position;
            }
        }
        return position;
    };
    if (element instanceof Document) {
        return '/';
    }
    for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {
        comp = comps[comps.length] = {};
        switch (element.nodeType) {
            case Node.TEXT_NODE:
                comp.name = 'text()';
                break;
            case Node.ATTRIBUTE_NODE:
                comp.name = '@' + element.nodeName;
                break;
            case Node.PROCESSING_INSTRUCTION_NODE:
                comp.name = 'processing-instruction()';
                break;
            case Node.COMMENT_NODE:
                comp.name = 'comment()';
                break;
            case Node.ELEMENT_NODE:
                comp.name = element.nodeName;
                comp.attribute = '';
                attrs=[];
                // if (comp.name) {
                //     break;
                // }
                if (element.getAttribute('id') != null && element.getAttribute('id') != '') {
                    attrs.push("@id='" + element.getAttribute('id') + "'");
                }
                if (element.getAttribute('class') != null && element.getAttribute('class') != '') {
                    attrs.push("@class='" + element.getAttribute('class') + "'");
                }
                for (i = 0; i < attrs.length; ++i) {
                    if (i > 0) {
                        comp.attribute += 'or';
                    }
                    comp.attribute += attrs[i];
                }
                break;
        }
        comp.position = getPos(element);
    }
    for (var i = comps.length - 1; i >= 0; i--) {
        comp = comps[i];
        xpath += '/' + comp.name.toLowerCase();
        if (comp.position !== null) {
            // xpath += '[' + comp.position + ']';
            if (comp.attribute == ''||comp.name == 'HTML') {
                xpath += '[' + comp.position + ']';
            }
            else xpath += '[' + comp.position + '][' + comp.attribute + ']';
        }
    }
    return xpath;
}
return absoluteXPath(arguments[0]);