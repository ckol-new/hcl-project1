import tkinter as tk
from tkinter import ttk
from py.model.QueryPipeline import QueryPipeline
from tkinter.font import Font


class GUI:
    MEDIUM_PADDING = 5
    LARGE_PADDING = 10
    def __init__(self):
        # get query pipeline
        self.query_pipeline = QueryPipeline()

        #TODO replace this with gui selection of database
        self.db = (
            r'C:\Users\wslam\Everything\health_city_lab\project1\hcl-project\src\data\Embed_Output\ALZConnected\dementia_or_other_embedding.jsonl',
            r'C:\Users\wslam\Everything\health_city_lab\project1\hcl-project\src\data\Embed_Output\ALZConnected\early_onset_embedding.jsonl'
                   )


        # initialize window
        self.__root = tk.Tk()
        self.style = Font(size=12, family='Times New Roman')

        # set title
        self.__root.title('Dementia Bot')

        # set geometry
        self.set_geometry()

        # set ui
        self.ui_frame, self.query_entry, self.top_N_entry, self.top_K_entry = self.set_ui_frame(
            pos=(0, 0),
            span=(5, 2)
        )

        # set result view
        self.result_view = self.set_text_view(
            pos=(0, 2),
            span=(5, 2)
        )

        # main loop
        self.__root.mainloop()

    def set_geometry(self, size: tuple = (1200, 1000), min_size: tuple = (800, 600)):
        self.__root.geometry(f'{size[0]}x{size[1]}')
        self.__root.minsize(min_size[0], min_size[1])
        self.__root.resizable(width=True, height=True)

    def set_ui_frame(self,  pos: tuple, span: tuple) -> (ttk.Frame, ttk.Entry, ttk.Entry, ttk.Entry):
        frame = ttk.Frame(
            self.__root,
            padding='10'
        )
        # set buttons
        self.set_button(frame, 'QUERY', (0, 0), (1, 1), self.run_query)
        self.set_button(frame, 'CLEAR', (1, 0), (1, 1), self.clear_text_view)

        # set labels
        self.set_label(frame, 'query: ', (0, 1), (1, 1))
        self.set_label(frame, 'top-N: ', (1, 1), (1, 1))
        self.set_label(frame, 'top-K: ', (2, 1), (1, 1))

        # set entries
        query_text_entry = self.set_entry(frame, (0, 2), (1, 2))
        top_N_entry = self.set_entry(frame, (1, 2), (1, 2))
        top_K_entry = self.set_entry(frame, (2, 2), (1, 2))

        # set defaults for entries
        top_N_entry.insert(0, '50')
        top_K_entry.insert(0, '5')

        frame.grid(
            row=pos[0], column=pos[1],
            rowspan=span[0], columnspan=span[1]
        )

        return frame, query_text_entry, top_N_entry, top_K_entry

    def set_text_view(self, pos: tuple, span: tuple) -> tk.Text:
        frame = ttk.Frame(
            self.__root,
            padding='10'
        )

        # set scroll bar
        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL
        )
        scrollbar.grid(row=0, column=0)

        # set text view
        textview = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=self.style)
        textview.grid(row=0, column=1, sticky='nsew')
        scrollbar.config(command=textview.yview)

        # set frame
        frame.grid(
            row=pos[0], column=pos[1],
            rowspan=span[0], columnspan=span[1]
        )

        return textview


    def set_entry(self, frame, pos: tuple, span: tuple) -> ttk.Entry:
        entry = ttk.Entry(
            frame,
        )
        entry.grid(
            row=pos[0], column=pos[1],
            rowspan=span[0], columnspan=span[1],
            padx=GUI.MEDIUM_PADDING, pady=GUI.MEDIUM_PADDING,
            ipadx=GUI.MEDIUM_PADDING, ipady=GUI.MEDIUM_PADDING,
            sticky=''
        )
        return entry

    def set_label(self, frame, text: str, pos: tuple, span: tuple):
        tk.Label(
            frame,
            text=text,
            padx=GUI.MEDIUM_PADDING, pady=GUI.MEDIUM_PADDING,
            font=self.style
        ).grid(
            row=pos[0], column=pos[1],
            rowspan=span[0], columnspan=span[1],
            padx=GUI.MEDIUM_PADDING, pady=GUI.MEDIUM_PADDING,
        )

    def set_button(self, frame, text: str, pos: tuple, span: tuple, action):
        tk.Button(
            frame,
            text=text,
            command=action,
            padx=GUI.MEDIUM_PADDING, pady=GUI.MEDIUM_PADDING,
            font=self.style
        ).grid(
            row=pos[0], column=pos[1],
            rowspan=span[0], columnspan=span[1],
            sticky='nsew'
        )

    def run_query(self):
        # get query text
        if not self.query_entry.get(): return
        query_text = self.query_entry.get()
        print(query_text)

        # get parameters
        if not self.top_K_entry.get(): return
        if not self.top_N_entry.get(): return
        try:
            top_N = int(self.top_N_entry.get())
            top_K = int(self.top_K_entry.get())
        except TypeError as e:
            print(e)
            return

        # do query
        results = self.query_pipeline.multi_query(
            query_text,
            *self.db,
            top_n=top_N,
            top_k=top_K
        )

        self.result_view.insert(tk.END, '*****************************************************\n')
        self.result_view.insert(tk.END, query_text + '\n')
        self.result_view.insert(tk.END, '*****************************************************\n')

        outputs = self.query_pipeline.display_result(results)
        self.show_results(outputs)



    def show_results(self, outputs: list[str]):
        for line in outputs:
            self.result_view.insert(tk.END, line + '\n')


    def clear_text_view(self):
        self.result_view.delete('1.0', tk.END)



gui = GUI()