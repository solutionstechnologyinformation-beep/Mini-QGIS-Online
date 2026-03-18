import csv
import io
from .spatial import convert

def process_coordinate_file(file_content, src_epsg, dst_epsg):
    results = []
    # Usar StringIO para tratar o conteúdo do arquivo como um arquivo real
    f = io.StringIO(file_content)
    reader = csv.reader(f, delimiter=",") # Assumindo CSV com vírgula como delimitador

    # Ignorar cabeçalho se houver (assumindo que a primeira linha pode ser cabeçalho)
    # Ou adicionar lógica para detectar se há cabeçalho
    header = next(reader, None) # Lê a primeira linha, se existir
    if header and not all(h.replace('.', '', 1).isdigit() or (h.startswith('-') and h[1:].replace('.', '', 1).isdigit()) for h in header): # Verifica se o cabeçalho não é numérico
        # É um cabeçalho, então vamos usá-lo ou ignorá-lo
        pass
    else:
        # Não é um cabeçalho, é a primeira linha de dados, então a processamos
        if header: # Se havia uma linha lida, ela é a primeira linha de dados
            try:
                x = float(header[0])
                y = float(header[1])
                converted_x, converted_y = convert(x, y, src_epsg, dst_epsg)
                results.append({"original_x": x, "original_y": y, "converted_x": converted_x, "converted_y": converted_y})
            except (ValueError, IndexError):
                # Ignorar linha mal formatada ou com menos de 2 colunas
                pass

    for row in reader:
        try:
            # Assumindo que as coordenadas X e Y estão nas duas primeiras colunas
            x = float(row[0])
            y = float(row[1])
            converted_x, converted_y = convert(x, y, src_epsg, dst_epsg)
            results.append({"original_x": x, "original_y": y, "converted_y": converted_y, "converted_x": converted_x})
        except (ValueError, IndexError):
            # Ignorar linhas mal formatadas ou com menos de 2 colunas
            continue
    return results

def format_results_for_export(results):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["original_x", "original_y", "converted_x", "converted_y"])
    for row in results:
        writer.writerow([row["original_x"], row["original_y"], row["converted_x"], row["converted_y"]])
    return output.getvalue()
