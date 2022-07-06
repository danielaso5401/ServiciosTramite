$(function()
{
    $("#myTable").on('click','.delete',function(){    

        var currentRow=$(this).closest("tr");
        var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        $.ajax({
            type: "POST",
            url:'http://127.0.0.1:5000/delete_tramite/'+col1,
            success: function(){
                alert("se elimino correctamente");
            }
        })
    })
    $('#create').click(function(){
        var valor = document.getElementById("idTramite").value;
        var valor2 = document.getElementById("Tramiteremitente").value;
        var valor3 = document.getElementById("Tramiteasunto").value;
        var valor4 = document.getElementById("Tramiteredestino").value;
        var valor5 = document.getElementById("Tramitefecha").value;
        
        $.ajax({
            type: "POST",
            url:'http://127.0.0.1:5000/create_tramite',
            data:JSON.stringify({
                "idTramite":valor,
                "Tramiteremitente":valor2,
                "Tramiteasunto":valor3,
                "Tramiteredestino":valor4,
                "Tramitefecha":valor5
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: function(){
                alert("se ingreso correctamente");
            }
        })
        
    })
    $("#myTable").on('click','.update',function(){    
    
        var currentRow=$(this).closest("tr");
        var col1=currentRow.find("td:eq(0)").text();
        var col2=currentRow.find("td:eq(1)").text(); 
        var col3=currentRow.find("td:eq(2)").text(); 
        var col4=currentRow.find("td:eq(3)").text();
        var col5=currentRow.find("td:eq(4)").text();
        $.ajax({
            type: "POST",
            url:'http://127.0.0.1:5000/update_tramite/'+col1,
            data:JSON.stringify({
                "name":col2,
                "fecha":col3,
                "destino":col4,
                "asunto":col5
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: function(){
                alert("se actualizo correctamente");
            }
        })
    })
}

)