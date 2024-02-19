from fastapi import HTTPException
import src.db.firebase_config as firebase_config


def register_user(username):
    data = {"cnt":0}
    firebase_config.db.child("payment").child(username).set(data)
    return "Usuario registrado!"


def add_payment_method(username, type, id):
    try:        
        #Validate username
        registered = False
        users = firebase_config.db.child("payment").get().val()

        for user in users:
            if username == user:
                registered = True
        
        if not registered:
            raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
        
        #Validate type
        if type not in {"pix", "boleto", "debito", "credito"}:
            raise HTTPException(status_code=400, detail="Forma de pagamento invalida!")
        
        #Validate type:key association
        if id == None and type not in {"pix", "boleto"}:
            raise HTTPException(status_code=400, detail="Essa forma de pagamento demanda um numero de id.")
        
        elif id != None and type in {"pix", "boleto"}:
            raise HTTPException(status_code=400, detail="Essa forma de pagamento nao deve apresentar um numero de id.")
        
        elif type in {"debito", "credito"}:
            splt_str = id.split()

            for string in splt_str:
                if len(string) != 4 or len(splt_str) != 4:
                    raise HTTPException(status_code=400, detail="Numero de id informado nao eh valido!")

        #Check if payment method is already registered
        cnt = firebase_config.db.child("payment").child(username).child("cnt").get().val()
        
        if cnt != 0:
            for i in range(cnt+1):
                method = "method" + str(i)
                method_type = firebase_config.db.child("payment").child(username).child(method).child("type").get().val()
                method_id = firebase_config.db.child("payment").child(username).child(method).child("id").get().val()

                if method_id == id and id == None and method_type == type:
                    raise HTTPException(status_code=409, detail="Essa forma de pagamento ja esta registrada!")
                elif method_id == id:
                    raise HTTPException(status_code=409, detail="Ja existe uma forma de pagamento registrada com esse id.")

        #Check payment method limit
        cnt = firebase_config.db.child("payment").child(username).child("cnt").get().val()
        
        if cnt == 3:
            raise HTTPException(status_code=400, detail="Limite de formas de pagamento atingido!")
        
        #Updating payment method count and registering data 
        cnt += 1
        cnt_s = str(cnt)

        data = {
            "type": type,
            "id": id
        }
        firebase_config.db.child("payment").child(username).child("cnt").set(cnt)
        firebase_config.db.child("payment").child(username).child("method"+cnt_s).set(data)

    except HTTPException as hex:
        raise hex
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

def update_payment_method(username, method, type, id):
    try:
        cur_id = firebase_config.db.child("payment").child(username).child(method).child("id").get().val()
        cur_type = firebase_config.db.child("payment").child(username).child(method).child("type").get().val()

        if type == "foo":
            type = cur_type
        if id == "foo":
            id = cur_id

        #Validate username
        registered = False
        users = firebase_config.db.child("payment").get().val()

        for user in users:
            if username == user:
                registered = True
        
        if not registered:
            raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
        
        #Validate method
        registered = False
        methods = firebase_config.db.child("payment").child(username).get().val()

        for reg_method in methods:
            if method == reg_method:
                registered = True
        
        if not registered:
            raise HTTPException(status_code=404, detail="Forma de pagamento nao encontrada!")
        
        #Validate type
        if type not in {"pix", "boleto", "debito", "credito", "foo"}:
            raise HTTPException(status_code=400, detail="Forma de pagamento invalida!")
        
        #Check if payment method is already registered
        cnt = firebase_config.db.child("payment").child(username).child("cnt").get().val()
        
        if cnt != 0:
            for i in range(cnt+1):
                key = "method" + str(i)
                method_type = firebase_config.db.child("payment").child(username).child(key).child("type").get().val()
                method_id = firebase_config.db.child("payment").child(username).child(key).child("id").get().val()

                if method != key:
                    if method_id == id and id == None and method_type == type:
                        raise HTTPException(status_code=409, detail="Essa forma de pagamento ja esta registrada!")
                    elif method_id == id and id != None:
                        raise HTTPException(status_code=409, detail="Ja existe uma forma de pagamento registrada com esse id.")

        #Validate update
        if type in {"debito", "credito"}:
            if id == None:
                raise HTTPException(status_code=400, detail="Essa forma de pagamento demanda um numero de id.")
            
            else:
                splt_str = id.split()

                for string in splt_str:
                    if len(string) != 4 or len(splt_str) != 4:
                        raise HTTPException(status_code=400, detail="Numero de id informado eh invalido")

                data = {"type": type,
                        "id": id}
                
        else:
            data = {"type": type,
                    "id": None}
        
        firebase_config.db.child("payment").child(username).child(method).set(data)

    except HTTPException as hex:
        raise hex
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


def delete_payment_method(username, method):
    try:
        #Validate username
        registered = False
        users = firebase_config.db.child("payment").get().val()

        for user in users:
            if username == user:
                registered = True
        
        if not registered:
            raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
        
        #Validate method
        registered = False
        methods = firebase_config.db.child("payment").child(username).get().val()

        for reg_method in methods:
            if method == reg_method:
                registered = True
        
        if not registered:
            raise HTTPException(status_code=404, detail="Forma de pagamento nao encontrada!")
        
        #Deletion
        iter = int(method.removeprefix("method"))
        cnt = firebase_config.db.child("payment").child(username).child("cnt").get().val()

        for i in range(cnt-iter):
            cur_i = iter + i
            if (cur_i) < cnt:
                data = firebase_config.db.child("payment").child(username).child("method"+str(cur_i+1)).get().val()
                firebase_config.db.child("payment").child(username).child("method"+str(cur_i)).update(data)
        
        firebase_config.db.child("payment").child(username).child("method"+str(cnt)).set({})
        cnt -= 1
        firebase_config.db.child("payment").child(username).update({"cnt": cnt})

    except HTTPException as hex:
        raise hex
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    