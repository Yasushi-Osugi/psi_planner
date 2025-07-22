# node_base.py
from typing import List, Optional, Callable

class BaseNode:
    def __init__(self, name: str):
        self.name = name
        self.children: List['BaseNode'] = []
        self.parent: Optional['BaseNode'] = None

    def add_child(self, child: 'BaseNode'):
        self.children.append(child)
        child.parent = self

    def iter_nodes(self):
        yield self
        for child in self.children:
            yield from child.iter_nodes()

    def find_node(self, condition: Callable[['BaseNode'], bool]) -> Optional['BaseNode']:
        for node in self.iter_nodes():
            if condition(node):
                return node
        return None

    def find_all(self, condition: Callable[['BaseNode'], bool]) -> List['BaseNode']:
        return [node for node in self.iter_nodes() if condition(node)]

    def count_nodes(self, condition: Callable[['BaseNode'], bool] = lambda x: True) -> int:
        return sum(1 for node in self.iter_nodes() if condition(node))


class PlanNode(BaseNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.sku_dict = {}  # SKU�� -> PlanNode�i����SKU�j
        self.psi4demand = None  # �T��PSI�\��: [[[] for j in range(4)] for w in range(�T��)]
        self.psi4supply = None
        self.lead_time = 0  # ��: ���[�h�^�C���A�K�v�ɉ����Ċg��
        self.capacity = None  # ��: ���Y�E�A���L���p�V�e�B
        # ���ɂ�slot list, backlog, allocation�Ȃǂ������I�ɒǉ��\


class GUINode(BaseNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.position = (0, 0)  # GUI��̍��W�ix, y�j
        self.color = "#ffffff"  # �m�[�h�̕\���F
        self.folded = False  # GUI�c���[�̓W�J/�܂肽���ݏ��
        self.selected = False  # �I�����
        # GUI�`��p�̃��x���A�\���p�L���v�V�����Ȃǂ��g���\
