import base64, marshal, zlib

def hide_my_code(input_file, output_file):
    try:
        # 1. Оригинал кодыг унших
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        # 2. Bytecode болгож compile хийх
        compiled_code = compile(source_code, input_file, 'exec')
        
        # 3. Marshal-аар цуваанд оруулж, Zlib-ээр шахаж, Base64-өөр шифрлэх
        marshaled = marshal.dumps(compiled_code)
        compressed = zlib.compress(marshaled)
        encoded = base64.b64encode(compressed).decode()
        
        # 4. Ажиллуулах бүрхүүл код
        final_code = f"# Encrypted by SEREK69\nimport marshal,zlib,base64;exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"
        
        with open(output_file, 'w') as f:
            f.write(final_code)
        print(f"✅ {input_file} -> {output_file} [АМЖИЛТТАЙ]")
    except Exception as e:
        print(f"❌ Алдаа ({input_file}): {e}")

# ХОЁР ФАЙЛЫГ ХОЁУЛАНГ НЬ НУУЦЛАХ
hide_my_code('tool.py', 'tool_hidden.py')
hide_my_code('bot.py', 'bot_hidden.py')

