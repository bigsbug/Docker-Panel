import datetime
import json
from mimetypes import init
from django.shortcuts import redirect, render
from django.contrib import messages
from dateutil.parser import parse
from django.http import HttpRequest, HttpResponse, JsonResponse
import docker
import docker.errors
from django.views.decorators.csrf import csrf_exempt

client = docker.from_env()
from docker.models.containers import Container


class ContainerInfo:
    def __init__(self, container: Container) -> None:
        self.container = container

    def id(self) -> str:
        return self.container.id

    def name(self) -> str:
        return self.container.attrs["Name"][1::]

    def status(self) -> str:
        return self.container.attrs["State"]["Status"]

    def image(self) -> str:
        return self.container.image.tags[0].split(":")[0]

    def tags(self) -> str:
        return self.container.image.tags[0].split(":")[1]

    def created_time(self) -> datetime.datetime:
        created_time = self.container.attrs["Created"]
        datetime_object = parse(created_time)
        date_format = r"%Y-%m-%d %H:%M:%S"
        return datetime_object.strftime(date_format)

    def platform(self) -> str:
        return self.container.attrs["Platform"]

    def driver(self) -> str:
        return self.container.attrs["Driver"]

    def restart_count(self) -> int:
        restart_count = int(self.container.attrs["RestartCount"])
        return restart_count

    def is_on(self):
        return self.status() == "running"

    def is_off(self):
        return self.status() == "exited"


class Docker_Container:
    def __init__(self, id) -> None:
        self.id = id

    def __Get_Container(self):
        try:
            self.container = client.containers.get(self.id)
        except docker.errors.NotFound:
            return False
        return True

    def SetUp(self):
        if self.__Get_Container():
            self.container_info = ContainerInfo(self.container)
        else:
            return False
        return True

    def Restart(self):
        self.container.reload()
        return True

    def Start(self):

        self.container.start()
        return True

    def Stop(self):
        self.container.kill()
        return True

    def Remove(self):
        self.container.remove()
        return True


def Home(request):
    template = "html/home.html"
    containers = client.containers.list(all=True)
    info_containers = [ContainerInfo(container) for container in containers]

    context = {"containers": info_containers}
    return render(request, template, context)


def Container(request, id):
    template = "html/container.html"
    container = Docker_Container(id)
    if container.SetUp():
        context = {
            "container": container.container_info,
        }
        return render(request, template, context)
    messages.warning(request, "Container NotFound")
    redirect("Panel:Home")


@csrf_exempt
def Create_Container(request: HttpRequest):
    data = request.body.decode("utf-8")
    json_data = json.loads(data)
    name = json_data.get("name", None)
    image = json_data.get("image", None)
    detach = json_data.get("detach", False)
    if name and image:
        container = client.containers.run(image, name=name, detach=detach)
        result = {"Success": "Container Created Successfuly"}
    else:
        result = {"Error": "Please fill all inputs"}
    print(name, image, detach)
    return JsonResponse(result)


def Delete_Container(request, id):
    container = Docker_Container(id)
    if container.SetUp():
        container.Remove()
    else:
        messages.warning(request, "Container Not Found")
    return redirect("Panel:Home")


def Update_Container(request, id):
    pass


def toggle_turn_OffOn(request, id):
    container = Docker_Container(id)
    if container.SetUp():
        print(container.container_info.status())
        if container.container_info.is_on():
            container.Stop()
            messages.info(
                request,
                f"Container {container.container_info.name()} stoped",
            )
        elif container.container_info.is_off():
            container.Start()
            messages.info(
                request,
                f"Container {container.container_info.name()} startd",
            )
        else:
            messages.warning(
                request,
                "Error This operation could not be performed",
            )

    return redirect("Panel:Home")


def Restart_Container(request, id):
    container = Docker_Container(id)
    if container.SetUp():
        container.Restart()
        messages.info(request, "Container Restarted Sucessfuly")
    else:
        messages.warning(request, "Container Not Found")

    return redirect("Panel:Home")
