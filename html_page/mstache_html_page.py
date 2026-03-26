from __future__ import annotations
import mstache
import os
from dataclasses import dataclass




@dataclass(frozen=True, slots=True)
class MstacheHtmlPage:
    template_path: str
    data: dict

    def with_data(self, name: str, value) -> MstacheHtmlPage:
        if name == "product":
            # Исправляем: проверяем наличие ключа "products"
            if 'products' not in self.data:
                self.data['products'] = []
            
            self.data['products'].append(value)
        else:
            # Для других типов данных
            self.data[name] = value
        
        return MstacheHtmlPage(self.template_path, self.data)
    
    def display(self) -> str:
        template_path = os.path.join("templates", self.template_path)
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        return mstache.render(template, self.data)
    
    def new(template: str) ->  MstacheHtmlPage:
        return  MstacheHtmlPage(template, {})