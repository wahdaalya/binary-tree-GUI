import tkinter as tk
from tkinter import simpledialog
import cv2
from PIL import Image, ImageTk
import os

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self): 
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if not node:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        return node

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if not node:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
        return result

    def preorder(self):
        return self._preorder(self.root, [])

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result

    def postorder(self):
        return self._postorder(self.root, [])

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
        return result

ASSET_FOLDER = os.path.dirname(__file__)
BOLA_IMAGE_PATH = os.path.join(ASSET_FOLDER, 'bola_sihir.png')
BG_VIDEO_PATH = os.path.join(ASSET_FOLDER, 'background.mp4')

class BinaryTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisasi Pohon Biner")
        self.tree = BinaryTree()

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        if not os.path.exists(BOLA_IMAGE_PATH):
            print(f"Gambar tidak ditemukan: {BOLA_IMAGE_PATH}")
            return
        if not os.path.exists(BG_VIDEO_PATH):
            print(f"Video tidak ditemukan: {BG_VIDEO_PATH}")
            return

        self.bola_img = Image.open(BOLA_IMAGE_PATH).resize((60, 60))
        self.bola_img = ImageTk.PhotoImage(self.bola_img)

        self.cap = cv2.VideoCapture(BG_VIDEO_PATH)
        self.update_background()

        self.create_buttons()
        self.draw_tree()

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.place(x=10, y=10)

        tk.Button(frame, text="Insert", command=self.insert_node).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Delete", command=self.delete_node).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Inorder", command=self.traverse_inorder).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Preorder", command=self.traverse_preorder).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Postorder", command=self.traverse_postorder).pack(side=tk.LEFT, padx=5)

    def insert_node(self):
        value = simpledialog.askinteger("Insert", "Masukkan angka:")
        if value is not None:
            self.tree.insert(value)
            self.draw_tree()

    def delete_node(self):
        value = simpledialog.askinteger("Delete", "Masukkan angka yang ingin dihapus:")
        if value is not None:
            self.tree.delete(value)
            self.draw_tree()

    def traverse_inorder(self):
        hasil = self.tree.inorder()
        print("Inorder:", hasil)

    def traverse_preorder(self):
        hasil = self.tree.preorder()
        print("Preorder:", hasil)

    def traverse_postorder(self):
        hasil = self.tree.postorder()
        print("Postorder:", hasil)

    def draw_tree(self):
        self.canvas.delete("node")
        if self.tree.root:
            self._draw_node(self.tree.root, 400, 100, 200, None)

    def _draw_node(self, node, x, y, dx, parent_coords):
        radius = 35 
        if node.left:
            self._draw_node(node.left, x - dx, y + 100, dx // 2, (x, y))
        if node.right:
            self._draw_node(node.right, x + dx, y + 100, dx // 2, (x, y))

        if parent_coords:
            self.canvas.create_line(parent_coords[0], parent_coords[1] + radius, x, y - radius, width=4, fill="#212162", tags="node")

        self.canvas.create_image(x, y, image=self.bola_img, tags="node")
        self.canvas.create_text(x, y + 2, text=str(node.value), fill='white', font=('Helvetica', 14, 'bold'), tags="node")

    def update_background(self):
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(BG_VIDEO_PATH)

        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            self.cap = cv2.VideoCapture(BG_VIDEO_PATH)
            ret, frame = self.cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (800, 600))
            img = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.delete("bg")
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW, tags="bg")
            self.canvas.tag_lower("bg")

        self.root.after(30, self.update_background)

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeGUI(root)
    root.mainloop()
