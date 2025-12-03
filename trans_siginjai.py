import networkx as nx
import matplotlib.pyplot as plt

def main():
    # --- BAGIAN 1: INISIALISASI GRAF & DATA ---
    print("Memulai Inisialisasi Peta Trans Siginjai (Satuan Meter)...")
    
    G = nx.Graph()

    # Daftar Lokasi (Node)
    nodes = [
        "Pijoan", "Simpang Rimbo", "Alam Barajo", 
        "UNJA Telanai", "Simpang BI", "Jamtos", 
        "Sipin", "Pasar (WTC)"
    ]
    G.add_nodes_from(nodes)

    # Daftar Jalan & Jarak (Edge & Weight) 
    # SEMUA SUDAH DIKONVERSI KE METER (x1000) AGAR KONSISTEN
    rute_jalan = [
        ("Pijoan", "Simpang Rimbo", 12100),   # 12.1 km -> 12100 m
        ("Simpang Rimbo", "Alam Barajo", 2700),    # 2.7 km -> 2700 m
        ("Simpang Rimbo", "UNJA Telanai", 5200),   # 5.2 km -> 5200 m
        ("Alam Barajo", "Jamtos", 6700),           # 6.7 km -> 6700 m
        
        # --- PERUBAHAN REQUEST ANDA DI SINI ---
        ("UNJA Telanai", "Simpang BI", 500),       # Hanya 500 meter
        # --------------------------------------

        ("Simpang BI", "Sipin", 2100),             # 2.1 km -> 2100 m
        ("Jamtos", "Sipin", 3100),                 # 3.1 km -> 3100 m
        ("Sipin", "Pasar (WTC)", 6500),            # 6.5 km -> 6500 m
        ("UNJA Telanai", "Pasar (WTC)", 5400),     # 5.4 km -> 5400 m
        ("Alam Barajo", "Simpang BI", 7800)        # 7.8 km -> 7800 m
    ]
    
    G.add_weighted_edges_from(rute_jalan)

    # --- BAGIAN 2: ALGORITMA DIJKSTRA ---
    
    start_node = "Pijoan"
    end_node = "Pasar (WTC)"
    
    print(f"\nMencari rute tercepat dari '{start_node}' ke '{end_node}'...")

    try:
        # Hitung jalur (list nama tempat)
        shortest_path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
        
        # Hitung total jarak (angka)
        total_distance = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')

        # Tampilkan Hasil di Terminal
        print("\n" + "="*40)
        print("HASIL REKOMENDASI RUTE (DIJKSTRA)")
        print("="*40)
        print(f"Jalur Terpilih: {' -> '.join(shortest_path)}")
        # Ubah tampilan hasil total jadi KM biar lebih enak dibaca, atau tetap meter
        print(f"Total Jarak   : {total_distance} meter ({total_distance/1000} km)") 
        print("="*40)

        # --- BAGIAN 3: VISUALISASI GRAF ---
        visualisasikan_peta(G, shortest_path)

    except nx.NetworkXNoPath:
        print("Error: Tidak ada jalur yang menghubungkan kedua lokasi tersebut.")

def visualisasikan_peta(G, path):
    plt.figure(figsize=(12, 7)) 

    # Layout Manual (Peta Jambi Barat -> Timur)
    pos = {
        "Pijoan": (-4, 0),
        "Simpang Rimbo": (-2, 0),
        "Alam Barajo": (-1, 1),     
        "UNJA Telanai": (-1, -1),   
        "Jamtos": (0.5, 1),
        "Simpang BI": (0.5, -1),
        "Sipin": (2, 0),
        "Pasar (WTC)": (4, 0)
    }

    # Gambar Jalan (Abu-abu putus-putus)
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2, style='dashed')
    
    # Gambar Halte (Biru)
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='#87CEEB', edgecolors='black')
    
    # Label Nama Halte
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', font_family='sans-serif')

    # Label Jarak (METER)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    # Di sini kita ubah formatnya jadi "m" atau "meter"
    edge_labels_fmt = {k: f"{v} m" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_fmt, font_size=8, font_color='gray')

    # --- HIGHLIGHT HASIL ---
    
    # Highlight Jalan Terpilih (Merah)
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#FF4500', width=4)
    
    # Highlight Halte Terpilih (Emas)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#FFD700', node_size=1600, edgecolors='black')

    plt.title("Visualisasi Rute Trans Siginjai (Satuan Meter)", fontsize=16, fontweight='bold', pad=20)
    plt.axis('off') 
    
    plt.tight_layout()
    plt.savefig("hasil_rute_siginjai_meter.png", dpi=300)
    print("\nGambar visualisasi disimpan sebagai 'hasil_rute_siginjai_meter.png'")
    plt.show()

if __name__ == "__main__":
    main()