import ollama
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from .models import Message

def chat_interface(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        return render(request, 'index.html', {'messages': messages})
    
def send_message(request):
    if request.method == 'POST':
        user_text = request.POST.get('message')
        
        if not user_text or not user_text.strip():
            return JsonResponse({'status': 'error', 'reply': 'A mensagem não pode estar vazia.'})
            
        Message.objects.create(role='user', content=user_text.strip())
        
        history = Message.objects.all().order_by('-timestamp')[:20]
        ollama_messages = [{'role': msg.role, 'content': msg.content} for msg in reversed(history)]
        
        personalidade = {
            'role': 'system',
            'content': 'Você é um engenheiro de software especialista. Responda sempre de forma técnica, vá direto ao ponto sem enrolação, e se escrever código, inclua comentários detalhados explicando a lógica.'
        }
        ollama_messages.insert(0, personalidade)

        def stream_generator():
            full_reply = ""
            try:
                stream = ollama.chat(model='llama3.1:8b', messages=ollama_messages, stream=True)
                for chunk in stream:
                    content = chunk['message']['content']
                    full_reply += content
                    yield content
            except Exception as e:
                yield f"\n[Erro de conexão com Ollama: {str(e)}]"
            finally:
                if full_reply:
                    Message.objects.create(role='assistant', content=full_reply)
        return StreamingHttpResponse(stream_generator(), content_type='text/plain')