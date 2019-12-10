import tkinter as tk
from tkinter import messagebox as msg
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk

class Lok_sabha(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1368x768')
        self.configure(bg='violet')
        self.title('Know Your PC')
        tk.Label(text="Parliamentary Election Data (With Graphs)",font="Arial 20 bold",bg="Orange",relief="sunken",pady=15).pack(side="top",fill="both")

        tk.Label(text='INSTRUCTIONS\n\n1. This Program will extract Parliamentary election information.\n2. The information extraction is done with regards of 2019,2014 and 2009 elections.\n3. The below three buttons will give Election data from three different Years.\n\n4. The Output will have Graphical Representation of the provided Parlimentary.\n5. The major focus of this Program is to compare Rank 1 and Rank 2 Candidates in provided Parliamentary.',font='Arial 12 bold',pady=15,padx=15,bg='#66ff66',relief="raised").pack(pady=30)


        self.elect_2019=tk.Button(text='For 2019 General Election',command=self.func_2019,font="timesnewroman 10 bold",width=25)
        self.elect_2019.pack(pady=20)
        self.elect_2019=tk.Button(text='For 2014 General Election',command=self.func_2014,font="timesnewroman 10 bold",width=25)
        self.elect_2019.pack()
        self.elect_2019=tk.Button(text='For 2009 General Election',command=self.func_2009,font="timesnewroman 10 bold",width=25)
        self.elect_2019.pack(pady=20)

        self.df=pd.read_csv(r'GE_india_2019_results.csv',encoding='cp1252')
        
        self.df.loc[:,'candidate_name']=self.df.loc[:,'candidate_name'].map(str.title)

        self.new_df=self.df.loc[self.df['rank']<3,:].set_index(['state/ut','PC'])


        self.df_2014=pd.read_csv(r"LS2014Candidate.csv")
        self.df_2014.loc[:,'Candidate Name']=self.df_2014.loc[:,'Candidate Name'].map(str.title)
        self.new_df_2014=self.df_2014.loc[self.df_2014['Position']<3,:].set_index(['State name','PC name'])
        one=self.new_df_2014.loc[self.new_df_2014['Position']==1,'Total Votes Polled']
        two=self.new_df_2014.loc[self.new_df_2014['Position']==2,'Total Votes Polled']
        minus=np.subtract(one,two)
        self.new_df_2014.loc[self.new_df_2014['Position']==2,'Votes_difference']=-minus
        self.new_df_2014.loc[self.new_df_2014['Position']==1,'Votes_difference']=minus


        self.df_2009=pd.read_csv(r"C:LS2009Candidate.csv")
        self.df_2009.loc[:,'Candidate Name']=self.df_2009.loc[:,'Candidate Name'].map(str.title)
        self.new_df_2009=self.df_2009.loc[self.df_2009['Position']<3,:].set_index(['State name','PC name'])
        one=self.new_df_2009.loc[self.new_df_2009['Position']==1,'Total Votes Polled']
        two=self.new_df_2009.loc[self.new_df_2009['Position']==2,'Total Votes Polled']
        minus=np.subtract(one,two)
        self.new_df_2009.loc[self.new_df_2009['Position']==2,'Votes_difference']=-minus
        self.new_df_2009.loc[self.new_df_2009['Position']==1,'Votes_difference']=minus

    def func_2019(self):
        child=tk.Tk()
        child.title('Elections 2019')
        child.attributes('-toolwindow',1)
        child.geometry('1920x1080')
        child.configure(bg='Lightgreen')
        tk.Label(child,text="Parliamentary Elections 2019",font="Arial 20 bold",bg="pink",relief="sunken").pack(side="top",fill="both")
        frame=tk.Frame(child,bg="orange",pady=50,padx=100)  # main frame
        frame.pack(side="top",pady=30)
        tk.Label(frame,text='Select Your State',font="timesnewroman 12 bold",bg='orange').grid(row=0,column=0,padx=20,pady=10)
        self.state=tk.StringVar()
        self.name_combo=ttk.Combobox(frame,textvariable=self.state,width=20,state='readonly',font="timesnewroman 10 bold")
        self.name_combo['values']=tuple(self.df.loc[:,'state/ut'].unique())
        # self.name_combo.current(4)
        self.name_combo.grid(row=0,column=1)

        tk.Label(frame,text='Total States and UT are',font="timesnewroman 12 bold",bg='orange').grid(row=2,column=0,padx=20,pady=10)
        tk.Label(frame,text=self.df.loc[:,'state/ut'].unique().size,font="timesnewroman 12 bold",bg='orange').grid(row=2,column=1)

        tk.Label(child,text='Note:-\tThe Submit button is used to get the result.',font="Arial 12 bold",bg="pink",relief="sunken",pady=20).pack(side='bottom',fill='both',pady=50)

        def load_pc(event=None):
            get_state=self.name_combo.get()
            tk.Label(frame,text='Select Your PC',font="timesnewroman 12 bold",bg='orange').grid(row=1,column=0)
            self.pc=tk.StringVar()
            self.pc_combo=ttk.Combobox(frame,textvariable=self.pc,width=20,state='readonly',font="timesnewroman 10 bold")
            self.pc_combo.grid(row=1,column=1)
            self.pc_combo['values']=tuple(sorted(self.new_df.reset_index(level=1).loc[get_state,'PC'].unique(),key=str.title))
            self.pc_combo.current(0)

            tk.Label(frame,text='Parliamentary are',font="timesnewroman 12 bold",bg='orange').grid(row=3,column=0)
            tk.Label(frame,text=self.new_df.reset_index(level=1).loc[get_state,'PC'].unique().size,font="timesnewroman 12 bold",bg='orange').grid(row=3,column=1)

            submit_button.configure(state='normal')
        # get_pc=tk.Button(child,text='Load PC',command=load_pc,font="timesnewroman 10 bold",width=10)
        # get_pc.pack()
        self.name_combo.bind("<<ComboboxSelected>>",load_pc)



        def plott():
            try:
                child2=tk.Tk()
                child2.geometry('1920x1080')
                child2.attributes('-toolwindow',1)
                child2.configure(bg='#ff5050')
                check_df=self.new_df.reset_index()
                fig = Figure(figsize=(25,3), dpi=90)
                fig2 = Figure(figsize=(25,3), dpi=70)
                ax = fig.add_subplot(1,2,2)
                ax2 = fig2.add_subplot(1,1,1)
                PC=self.pc_combo.get()
                get_state=self.name_combo.get()
                child2.title(f'{get_state} - {PC} - 2019')
                a=check_df.loc[(check_df['state/ut']==get_state)&(check_df['PC']==PC),:]
                a.reset_index().set_index('candidate_name').loc[:,['total_votes']].plot(kind='barh',ax=ax,title='Vote Comparison')
                show_label=tk.Label(child2,text=a.set_index('candidate_name').loc[:,['total_votes','party','votes_difference']],font='arial 12 bold',bg='#66ff66')
                show_label.pack(pady=10)
                a.reset_index().set_index('candidate_name').loc[:,['total_votes']].plot(kind='pie',ax=ax2,subplots=True,title='Vote Comparison')
                canvas = FigureCanvasTkAgg(fig, child2)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=20)
                canvas2 = FigureCanvasTkAgg(fig2, child2)
                canvas2.draw()
                canvas2.get_tk_widget().pack()
                def disable_event():
                    '''Disable close button at the top of window'''
                    pass
                child2.protocol("WM_DELETE_WINDOW",disable_event)
                def clear():
                    child2.destroy()
                clear_button=tk.Button(child2,text='Clear the Graph',font="timesnewroman 12 bold",width=20,command=clear)
                clear_button.pack(pady=15)
                child2.mainloop()
            except Exception as err:
                msg.showwarning('Warning','Wrong Combination of State and PC is used. Please Load PC again and then Submit.')
        def back():
            child.destroy()
        
        def disable_event():
            pass
        child.protocol("WM_DELETE_WINDOW",disable_event)
        submit_button=tk.Button(child,text="Submit",command=plott,font="timesnewroman 10 bold",width=10)
        submit_button.configure(state='disabled')
        submit_button.pack(pady=5)
        back_button=tk.Button(child,text="Back",command=back,font="timesnewroman 10 bold",width=10)
        back_button.pack(pady=5)
        
        child.mainloop()

    def func_2014(self):
        child=tk.Tk()
        child.title('Elections 2014')
        child.attributes('-toolwindow',1)
        child.geometry('1920x1080')
        child.configure(bg='#ff6666')
        tk.Label(child,text="Parliamentary Elections 2014",font="Arial 20 bold",bg="#00ace6",relief="sunken").pack(side="top",fill="both")
        frame=tk.Frame(child,bg="lightgreen",pady=50,padx=100)  # main frame
        frame.pack(side="top",pady=30)
        tk.Label(frame,text='Select Your State',font="timesnewroman 12 bold",bg='lightgreen').grid(row=0,column=0,padx=20,pady=10)
        self.state=tk.StringVar()
        self.name_combo=ttk.Combobox(frame,textvariable=self.state,width=20,state='readonly',font="timesnewroman 10 bold")
        self.name_combo['values']=tuple(sorted(self.df_2014.loc[:,'State name'].unique()))
        # self.name_combo.current(4)
        self.name_combo.grid(row=0,column=1)
        tk.Label(frame,text='Total States and UT are',font="timesnewroman 12 bold",bg='lightgreen').grid(row=2,column=0,padx=20,pady=10)
        tk.Label(frame,text=self.df_2014.loc[:,'State name'].unique().size,font="timesnewroman 12 bold",bg='lightgreen').grid(row=2,column=1)

        tk.Label(child,text='Note:-\tThe Submit button is used to get the result.',font="Arial 12 bold",bg="#00ace6",relief="sunken",pady=20).pack(side='bottom',fill='both',pady=50)

        def load_pc(event=None):
            get_state=self.name_combo.get()
            tk.Label(frame,text='Select Your PC',font="timesnewroman 12 bold",bg='lightgreen').grid(row=1,column=0)
            self.pc=tk.StringVar()
            self.pc_combo=ttk.Combobox(frame,textvariable=self.pc,width=20,state='readonly',font="timesnewroman 10 bold")
            self.pc_combo.grid(row=1,column=1)
            self.pc_combo['values']=tuple(sorted(self.new_df_2014.reset_index(level=1).loc[get_state,'PC name'].unique(),key=str.title))
            self.pc_combo.current(0)

            tk.Label(frame,text='Parliamentary are',font="timesnewroman 12 bold",bg='lightgreen').grid(row=3,column=0)
            tk.Label(frame,text=self.new_df_2014.reset_index(level=1).loc[get_state,'PC name'].unique().size,font="timesnewroman 12 bold",bg='lightgreen').grid(row=3,column=1)
            submit_button.configure(state='normal')

        # get_pc=tk.Button(child,text='Load PC',command=load_pc,font="timesnewroman 10 bold",width=10)
        # get_pc.pack()
        self.name_combo.bind("<<ComboboxSelected>>",load_pc)



        def plott():
            try:
                child2=tk.Tk()
                child2.geometry('1920x1080')
                child2.configure(bg='skyblue')
                check_df=self.new_df_2014.reset_index()
                child2.attributes('-toolwindow',1)
                
                fig = Figure(figsize=(25,3), dpi=90)
                fig2 = Figure(figsize=(25,3), dpi=70)
                ax = fig.add_subplot(1,2,2)
                ax2 = fig2.add_subplot(1,1,1)
                PC=self.pc_combo.get()
                get_state=self.name_combo.get()
                child2.title(f'{get_state} - {PC} - 2014')
                a=check_df.loc[(check_df['State name']==get_state)&(check_df['PC name']==PC),:]
                a.reset_index().set_index('Candidate Name').loc[:,['Total Votes Polled']].plot(kind='barh',ax=ax,color='y',title='Vote Comparison')
                show_label=tk.Label(child2,text=a.set_index('Candidate Name').loc[:,['Total Votes Polled','Party Abbreviation','Votes_difference']],font='arial 12 bold',bg='#ffc266')
                show_label.pack(pady=10)
                a.reset_index().set_index('Candidate Name').loc[:,['Total Votes Polled']].plot(kind='pie',ax=ax2,subplots=True,title='Vote Comparison')
                canvas = FigureCanvasTkAgg(fig, child2)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=20)
                canvas2 = FigureCanvasTkAgg(fig2, child2)
                canvas2.draw()
                canvas2.get_tk_widget().pack()
                def disable_event():
                    '''Disable close button at the top of window'''
                    pass
                child.protocol("WM_DELETE_WINDOW",disable_event)
                def clear():
                    child2.destroy()
                clear_button=tk.Button(child2,text='Clear the Graph',font="timesnewroman 12 bold",width=20,command=clear)
                clear_button.pack(pady=15)
                child2.mainloop()
            except Exception as err:
                msg.showwarning('Warning','Wrong Combination of State and PC is used. Please Load PC again and then Submit.')
        def back():
            child.destroy()
        
        def disable_event():
            pass
        child.protocol("WM_DELETE_WINDOW",disable_event)
        submit_button=tk.Button(child,text="Submit",command=plott,font="timesnewroman 10 bold",width=10)
        submit_button.configure(state='disabled')
        submit_button.pack(pady=5)
        back_button=tk.Button(child,text="Back",command=back,font="timesnewroman 10 bold",width=10)
        back_button.pack(pady=5)
        child.mainloop()

    def func_2009(self):
        child=tk.Tk()
        child.title('Elections 2009')
        child.attributes('-toolwindow',1)
        child.geometry('1920x1080')
        child.configure(bg='#6666ff')
        tk.Label(child,text="Parliamentary Elections 2009",font="Arial 20 bold",bg="#ff3300",relief="sunken").pack(side="top",fill="both")
        frame=tk.Frame(child,bg="#99cc00",pady=50,padx=100)  # main frame
        frame.pack(side="top",pady=30)
        tk.Label(frame,text='Select Your State',font="timesnewroman 12 bold",bg='#99cc00').grid(row=0,column=0,padx=20,pady=10)
        self.state=tk.StringVar()
        self.name_combo=ttk.Combobox(frame,textvariable=self.state,width=20,state='readonly',font="timesnewroman 10 bold")
        self.name_combo['values']=tuple(sorted(self.df_2009.loc[:,'State name'].unique()))
        # self.name_combo.current(4)
        self.name_combo.grid(row=0,column=1)
        tk.Label(child,text='Note:-\tThe Submit button is used to get the result.',font="Arial 12 bold",bg="#ff3300",relief="sunken",pady=20).pack(side='bottom',fill='both',pady=50)

        tk.Label(frame,text='Total States and UT are',font="timesnewroman 12 bold",bg='#99cc00').grid(row=2,column=0,padx=20,pady=10)
        tk.Label(frame,text=self.df_2009.loc[:,'State name'].unique().size,font="timesnewroman 12 bold",bg='#99cc00').grid(row=2,column=1)

        def load_pc(event=None):
            get_state=self.name_combo.get()
            tk.Label(frame,text='Select Your PC',font="timesnewroman 12 bold",bg='#99cc00').grid(row=1,column=0)
            self.pc=tk.StringVar()
            self.pc_combo=ttk.Combobox(frame,textvariable=self.pc,width=20,state='readonly',font="timesnewroman 10 bold")
            self.pc_combo.grid(row=1,column=1)
            self.pc_combo['values']=tuple(sorted(self.new_df_2009.reset_index(level=1).loc[get_state,'PC name'].unique(),key=str.title))
            self.pc_combo.current(0)
            tk.Label(frame,text=f'Parliamentary are',font="timesnewroman 12 bold",bg='#99cc00').grid(row=3,column=0)
            tk.Label(frame,text=self.new_df_2009.reset_index(level=1).loc[get_state,'PC name'].unique().size,font="timesnewroman 12 bold",bg='#99cc00').grid(row=3,column=1)

            submit_button.configure(state='normal')

        # get_pc=tk.Button(child,text='Load PC',command=load_pc,font="timesnewroman 10 bold",width=10)
        # get_pc.pack()
        self.name_combo.bind("<<ComboboxSelected>>",load_pc)


        def plott():
            try:
                child2=tk.Tk()
                child2.geometry('1920x1080')
                child2.configure(bg='#ff3399')
                child2.attributes('-toolwindow',1)
                check_df=self.new_df_2009.reset_index()
                
                
                fig = Figure(figsize=(25,3), dpi=90)
                fig2 = Figure(figsize=(25,3), dpi=70)
                ax = fig.add_subplot(1,2,2)
                ax2 = fig2.add_subplot(1,1,1)
                PC=self.pc_combo.get()
                get_state=self.name_combo.get()
                child2.title(f'{get_state} - {PC} - 2009')
                a=check_df.loc[(check_df['State name']==get_state)&(check_df['PC name']==PC),:]
                a.reset_index().set_index('Candidate Name').loc[:,['Total Votes Polled']].plot(kind='barh',ax=ax,color='g',title='Vote Comparison')
                show_label=tk.Label(child2,text=a.set_index('Candidate Name').loc[:,['Total Votes Polled','Party Abbreviation','Votes_difference']],font='arial 12 bold',bg='#66b3ff')
                show_label.pack(pady=10)
                a.reset_index().set_index('Candidate Name').loc[:,['Total Votes Polled']].plot(kind='pie',ax=ax2,subplots=True,title='Vote Comparison')
                canvas = FigureCanvasTkAgg(fig, child2)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=20)
                canvas2 = FigureCanvasTkAgg(fig2, child2)
                canvas2.draw()
                canvas2.get_tk_widget().pack()
                def disable_event():
                    '''Disable close button at the top of window'''
                    pass
                child.protocol("WM_DELETE_WINDOW",disable_event)
                def clear():
                    child2.destroy()
                clear_button=tk.Button(child2,text='Clear the Graph',font="timesnewroman 12 bold",width=20,command=clear)
                clear_button.pack(pady=15)
                child2.mainloop()
            except Exception as err:
                msg.showwarning('Warning','Wrong Combination of State and PC is used. Please Load PC again and then Submit.')
        def back():
            child.destroy()
        
        def disable_event():
            pass
        child.protocol("WM_DELETE_WINDOW",disable_event)
        submit_button=tk.Button(child,text="Submit",command=plott,font="timesnewroman 10 bold",width=10)
        submit_button.configure(state='disabled')
        submit_button.pack(pady=5)
        back_button=tk.Button(child,text="Back",command=back,font="timesnewroman 10 bold",width=10)
        back_button.pack(pady=5)
        child.mainloop()


if __name__ == "__main__":
    obj=Lok_sabha()
    obj.mainloop()
