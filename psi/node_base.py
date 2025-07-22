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
        self.sku_dict = {}  # SKU名 -> PlanNode（下位SKU）
        self.psi4demand = None  # 週次PSI構造: [[[] for j in range(4)] for w in range(週数)]
        self.psi4supply = None
        self.lead_time = 0  # 例: リードタイム、必要に応じて拡張
        self.capacity = None  # 例: 生産・輸送キャパシティ
        # 他にもslot list, backlog, allocationなども将来的に追加可能


class GUINode(BaseNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.position = (0, 0)  # GUI上の座標（x, y）
        self.color = "#ffffff"  # ノードの表示色
        self.folded = False  # GUIツリーの展開/折りたたみ状態
        self.selected = False  # 選択状態
        # GUI描画用のラベル、表示用キャプションなども拡張可能
