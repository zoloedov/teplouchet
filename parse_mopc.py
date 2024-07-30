# encoding: utf-8
import xml.etree.cElementTree as ET

f = "C:\\Users\\Zoloedov_is\\Desktop\\PyVKT\\vkt5-com_cut.m_opc"
# f = "C:\\Users\\Zoloedov_is\\Desktop\\PyVKT\\vkt5-com.m_opc"
f = "C:\\Users\\Zoloedov_is\\Desktop\\PyVKT\\tec-1.m_opc"
# f = "C:\\Users\\Zoloedov_is\\Desktop\\PyVKT\\test.m_opc"



class OpcTree:
    """ 

    """
    def __init__(self, filename):
        self._tags = []
        self._full_tags = []
        self._words = []
        self._xml = ET.parse(filename)
        self._root = self._xml.getroot()

    def _got_element(self, tree):
        """ Checks whether there is an iterable element in the tree.
            Returns boolean.

        """

        # According to pep8 bool(iterable) is better than bool(len(iterable)).
        # Empty iterable is False.
        return bool(tree.findall("./Element"))

    def _get_tags(self, tree, words):
        """ Recursively goes through the tree and gets full path of a 'leaf',
            parts of which are located in 'value' of Property nodes
            where 'name' is 'MasterOpc.NameInTree',
            e.g. <Property name="MasterOpc.NameInTree" value="link channel" />

        """
        prop = tree.findall("./Property[@name='MasterOpc.NameInTree']")[0]
        value = prop.attrib.get("value")
        words.append(value)
        if self._got_element(tree):
            for el in tree.findall("./Element"):
                self._get_tags(el, words[:])
        else:
            self._full_tags.append(":".join(words))

    def tags(self):
        """ Returns tag list ["Path:To:Tag1","Path:To:Another:Tag2", ...] """

        # _full_tags contain elements after previous tags() function call, clear it:
        self._full_tags = []
        self._get_tags(self._root, self._words)

        # Убираем всё до первого двоеточия, это название всей карты тэгов,
        # оно в построении имени тэга не участвует,
        # по крайней мере для чтения из OPC оно не нужно:
        self._tags = [tag[tag.find(":")+1:] for tag in self._full_tags]

        # Clear _words list, it must be empty before next call of _get_tags() inside tags() function:
        self._words = []
        return self._tags


if __name__ == "__main__":
    t = OpcTree(f)
    tags = t.tags()
    print("-------")
    for el in tags:
        print(el)
    print("%d tags"%len(tags))
    print("-------")

    # xml = ET.parse(f)
    # root = xml.getroot()
    # print root[-1][-1][-1][-2][-1][-1][-1].findall("./Property[@name='MasterOpc.NameInTree']")[0].attrib.get("value")
