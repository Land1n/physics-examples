import flet as ft

from flet.matplotlib_chart import MatplotlibChart

import matplotlib
import matplotlib.pyplot as plt

import re  

import math

matplotlib.use("svg")

def view_pop(e:ft.ViewPopEvent,*view):
    e.page.views.pop()
    top_view = e.page.views[-1]
    e.page.go(top_view.route)
    return top_view

class RoutersDict:
    def __init__(self,routers:dict = {}):
        self.routers = routers
    def __getitem__(self, route):
        if view:=self.routers.get(route,False):
            return view
        if any(key:=r for r in self.routers.keys() if (value := re.match(r,route))):
            return self.routers.get(key,False)
        return None

class Router:
    def __init__(self,page:ft.Page):
        self.page = page
        self.routes = RoutersDict({
            "/chart":ChartsView,
            "/parameters":ParametersView,
            "/task":TaskView,
        })

    def route_change(self,route):
        # if not [view for view in self.page.views if view.route == route.route]:
        self.page.views.append(self.routes[route.route](self.page))
        self.page.update()

class MainAppBar(ft.AppBar):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.title=ft.Text("Физика.Практика")
        self.actions=[
            ft.TextButton(text="Задача",on_click=lambda _:self.page.go("/task")),
            ft.TextButton(text="График",on_click=lambda _:self.page.go("/chart")),
            ft.TextButton(text="Параметры",on_click=lambda _:self.page.go("/parameters")),
        ]

class FrameCard(ft.Card):
    def __init__(self,control:ft.Control = None, title:ft.Text=None, leading:ft.Icon=None, actions:list[ft.Control]=None):
        
        self.col = ft.Column(tight=True)
        self.controls = self.col.controls

        if control != None:
            self.controls.append(control)

        row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(),
                ft.Row(tight=True)
            ]
        )
        if leading != None:
            row.controls[0].controls += [
                leading
            ]

        if title != None:
            row.controls[0].controls += [
                title
            ]

        if actions != None:
            row.controls[1].controls = actions

        if any([leading,title,actions]):
            self.controls.insert(0,row)

        super().__init__(
            content=ft.Container(
                padding=10,
                content=self.col,
            )
        )

class ChartsView(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.route = "/chart"
        self.appbar = MainAppBar(self.page)

        self.controls = [ft.ListView(expand=1)]

        for data in self.page.data:
            
            if data["parameters"] and data.get("function",False):
                fig, ax = plt.subplots(1,1)

                parameters = [data["parameters"][parameter]['val'] for parameter in data["parameters"]]
                
                print(parameters)

                x = [t for t in range(2,101)]
                y = [data["function"](*parameters,t=t) for t in range(2,101)]
                
                ax.plot(x,y)

                ax.set_xlabel('time')


                col = ft.Column(tight=True)

                col.controls.append(
                    ft.Text(f'Значание получившейся функции: {data["function"](*parameters,t=2)}',size=15,weight=ft.FontWeight.BOLD)
                )
                col.controls.append(
                    ft.Container(MatplotlibChart(fig),height=400)
                )

                if data.get("another_result",False):
                    col.controls.append(
                        ft.Divider()
                    )
                    for a_res in data["another_result"]:
                        if a_res["type"] == "chart":
                            fig1, ax1 = plt.subplots(1,1)
                            x1 = [t for t in range(2,101)]
                            parameters1 = [data["parameters"][parameter]['val'] for parameter in a_res["parameters"]]
                            y1 = [a_res["function"](*parameters1,t=t) for t in range(2,101)]
                            
                            ax1.set_title( a_res["label"])
                            ax1.plot(x1,y1)
                            col.controls.append(
                                ft.Text(a_res['label'],size=15,weight=ft.FontWeight.BOLD)
                            )
                            col.controls.append(
                                ft.Text(f'Значание получившейся функции: {a_res["function"](*parameters1,t=2)}',size=15,weight=ft.FontWeight.BOLD)
                            )
                            col.controls.append(
                                ft.Container(MatplotlibChart(fig1),height=400)
                            )
                        if a_res["type"] == "number":
                            parameters1 = [data["parameters"][parameter]['val'] for parameter in a_res["parameters"]]
                            col.controls.append(
                                ft.Text(a_res['label'],size=15,weight=ft.FontWeight.BOLD)
                            )
                            col.controls.append(
                                ft.Text(f'Значание получившейся функции: {a_res["function"](*parameters1)}',size=15,weight=ft.FontWeight.BOLD)
                            )
                    col.controls.append(
                        ft.Divider()
                    )
                self.controls[0].controls += [
                    FrameCard(
                        ft.ExpansionTile(
                            title=ft.Text(f"Задание номер: {data['title']}",size=15,weight=ft.FontWeight.BOLD),
                            controls=[col]
                        )
                    )
                ]

class ParametersView(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.route = "/parameters"
        self.appbar = MainAppBar(self.page)

        self.controls = [ft.ListView(expand=1)]

        for i,data in enumerate(self.page.data):        
            
            col = ft.Column(scroll=ft.ScrollMode.ALWAYS)

            for parameter in data["parameters"]:
                t = ft.Text(f"Значение параметра {parameter}: {data['parameters'][parameter]['val']}")
                col.controls.append(ft.Text(f"Параметр {parameter}:"))
                col.controls.append(
                    ft.Slider(
                        value=data["parameters"][parameter]['val'],
                        min=data["parameters"][parameter]['min'],
                        max=data["parameters"][parameter]['max'],
                        # divisions=data["parameters"][parameter]['step'],
                        label="10",
                        on_change_end=self.on_change_slider,
                        data={"t":t,"parameter":parameter,"i":i}
                    )
                )
                col.controls.append(t)
                col.controls.append(ft.Divider())
            self.controls[0].controls += [
                FrameCard(
                    ft.ExpansionTile(
                        title=ft.Text(f"Задание номер: {data['title']}",size=15,weight=ft.FontWeight.BOLD),
                        controls=[col],
                    )
                )
            ]
    def on_change_slider(self,e:ft.Control):
        e.control.data["t"].value = f"Значение параметра {e.control.data['parameter']}: {e.control.value}"
        self.page.data[e.control.data["i"]]["parameters"][e.control.data["parameter"]]["val"] = e.control.value
        self.page.update()

class TaskView(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.route = "/task"
        self.appbar = MainAppBar(self.page)

        self.controls = [ft.ListView(expand=1)]

        for data in self.page.data:
            image_list =[
                ft.Image(
                    src=image,
                    width=700,
                    fit=ft.ImageFit.CONTAIN,
                )
                for image in data['src']
            ]            
            
            image_list.insert(0,ft.Text("Задача:",size=20,weight=ft.FontWeight.BOLD))
            image_list.insert(2,ft.Divider())
            image_list.insert(3,ft.Text("Решение:",size=20,weight=ft.FontWeight.BOLD))

            self.controls[0].controls += [
                FrameCard(
                    ft.ExpansionTile(
                        title=ft.Text(f"Задание номер: {data['title']}",size=15,weight=ft.FontWeight.BOLD),
                        controls=image_list
                    )
                )
            ]

def main(page:ft.Page):

    page.theme_mode = "LIGHT"

    router = Router(page)
    page.on_route_change = router.route_change
    page.views.clear()
    page.data = [
        {
            "title":"1.213",
            "src":["images/1.2131.png","images/1.2132.png"],
            "parameters":{
                "n":{
                    "val":0,
                    "min":0,
                    "max":2,
                    "step":math.sqrt(2)
                }
            },
            "function": lambda n,t: t*1*(n**2-2)/(6-n**2)
        },
        {
            "title":"1.248",
            "src":["images/1.2481.png","images/1.2482.png"],
            "parameters":{
                "v0":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
                "l":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
                "Ms":{
                    "val":1.988416*10**30,
                    "min":10**30,
                    "max":3*10**30,
                    "step":0.001
                },
                "G":{
                    "val":6.67*10**(-11),
                    "min":10**(-11),
                    "max":10**(-10),
                    "step":10**(-11)
                }
            },
            "function": lambda v0,l,Ms,G,t: (G*Ms/v0**2)*(math.sqrt(1+(l*v0**2/G*Ms)**2) - 1)
        },
        {
            "title":"1.37",
            "src":["images/1.371.png","images/1.372.png"],
            "parameters":{
                "R":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
                "v0":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
                "s_for_w":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
        },
            "function": (lambda v0,R,s_for_w,t: v0/(1+(v0*t/R))),
            "another_result":[
                {   
                    "type":"chart",
                    "parameters":["R","v0"],
                    "label":"Скорость от расстояния",
                    "function":(lambda v0,R,t: v0*math.e**(-t/R))
                },
                {   
                    "type":"number",
                    "parameters":["R","v0","s_for_w"],
                    "label":"Полное ускорение",
                    "function":(lambda v0,R,s_for_w: math.sqrt(2)*(v0**2/R)*math.e**(-2*s_for_w/R))
                }
            ]
        },
        {
            "title":"1.377",
            "src":["images/1.3771.png","images/1.3772.png"],
            "parameters":{
                "w":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
                "l":{
                    "val":0.1,
                    "min":0.1,
                    "max":100,
                    "step":1
                },
                "h":{
                    "val":1.1,
                    "min":1.1,
                    "max":100,
                    "step":1
                },
            },
            "function": (lambda w,l,h,t: w*t*(2*l/(t-1))**0.5),
            "another_result":[
                {   
                    "type":"number",
                    "parameters":["w","l","h"],
                    "label":"Значение скорости с нашим параметром",
                    "function":(lambda w,l,h: w*h*(2*l/(h-1))**0.5)
                }
            ]
        },
        {
            "title":"1.1231",
            "src":["images/1.2311.png","images/1.2312.png"],
            "parameters":{
                "m":{
                    "val":0,
                    "min":0,
                    "max":100,
                    "step":1,
                },           
                "R":{
                    "val":0,
                    "min":0,
                    "max":100,
                    "step":1,
                },
                "a":{
                    "val":0,
                    "min":0,
                    "max":360,
                    "step":1,
                },           
                "g":{
                    "val":9.81,
                    "min":0,
                    "max":100,
                    "step":1,
                }    
            },
            "function": lambda m,g,R,a,t: m*g*R*math.sin(a*math.pi/180)*t
        },
    ]
    page.go("/task")

if __name__ == "__main__":
    ft.app(main,assets_dir="assets")