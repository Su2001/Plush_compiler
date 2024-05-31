from llvmlite import ir

class Environment:
    def __init__(self, records: dict[str, tuple[ir.Value, ir.Type]] = None, parent = None, name: str ="global") -> None:
        self.records: dict[str, tuple] = records if records else {}
        self.parent: Environment | None = parent
        self.name :str = name

    def define(self, name: str, value: ir.Value, _type: ir.Type) -> ir.Value:
        self.records[name] = (value, _type)
        return value
    
    def define_to(self, name: str, value: ir.Value, _type: ir.Type, targetname:str) -> ir.Value:
        if targetname != self.name:
            return self.parent.define_to(name,value,_type,targetname)
        else:
            self.records[name] = (value, _type)
        return value
    
    def lookup(self, name:str) -> tuple[ir.Value, ir.Type]:
        return self._resolve(name)
    
    def _resolve(self, name : str) -> tuple[ir.Value, ir.Type]:
        if name in self.records:
            return self.records[name]
        elif self.parent:
            return self.parent._resolve(name)
        return None