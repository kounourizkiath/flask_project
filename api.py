# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 11:07:52 2025

@author: 56036302
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 09:12:14 2025
@author: 56036302
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'dev'  # Nécessaire pour flash

DATABASE = 'ensembl_hs63_simple.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    parts = [row['atlas_organism_part'] for row in conn.execute(
        'SELECT DISTINCT atlas_organism_part FROM Expression ORDER BY atlas_organism_part limit 20'
    ).fetchall()]
    parts = [p for p in parts if p is not None]
    conn.close()
    return render_template('index.html', parts=parts)

@app.route('/parts/<part>/genes')
def genes(part):
    conn = get_db_connection()
    genes = conn.execute('''
        SELECT g.*,
               (SELECT t.ensembl_transcript_id
                FROM Transcripts t
                WHERE t.ensembl_gene_id = g.ensembl_gene_id
                ORDER BY t.ensembl_transcript_id
                LIMIT 1) AS first_transcript_id
        FROM Genes g
        JOIN Transcripts t2 ON g.ensembl_gene_id = t2.ensembl_gene_id
        JOIN Expression e ON t2.ensembl_transcript_id = e.ensembl_transcript_id
        WHERE e.atlas_organism_part = ?
        GROUP BY g.ensembl_gene_id
        ORDER BY g.ensembl_gene_id
        limit 20
    ''', (part,)).fetchall()
    conn.close()
    return render_template('genes.html', genes=genes, part=part)


@app.route('/parts/<part>/gene_names')
def gene_names(part):
    conn = get_db_connection()
    query = '''
        SELECT DISTINCT g.ensembl_gene_id, associated_gene_name
        FROM Genes as g
        NATURAL JOIN Transcripts as t
        NATURAL JOIN Expression as e
        WHERE e.atlas_organism_part = ?
        ORDER BY g.ensembl_gene_id
        limit 50
    '''
    genes = conn.execute(query, (part,)).fetchall()
    conn.close()
    return render_template('gene_names.html', genes=genes, part=part)

@app.route('/genes/<id>')
def gene_detail(id):
    conn = get_db_connection()
    gene_row = conn.execute('SELECT * FROM Genes WHERE ensembl_gene_id = ?', (id,)).fetchone()
    if gene_row is None:
        conn.close()
        return f"Gène {id} non trouvé.", 404

    gene = dict(gene_row)  # convert sqlite3.Row en dict

    transcripts = conn.execute('''
        SELECT ensembl_transcript_id, transcript_start, transcript_end
        FROM Transcripts
        WHERE ensembl_gene_id = ?
        ORDER BY ensembl_transcript_id
        limit 50
    ''', (id,)).fetchall()

    parts_rows = conn.execute('''
        SELECT DISTINCT e.atlas_organism_part
        FROM Expression e
        JOIN Transcripts t ON e.ensembl_transcript_id = t.ensembl_transcript_id
        WHERE t.ensembl_gene_id = ?
        ORDER BY e.atlas_organism_part
        limit 50
    ''', (id,)).fetchall()

    # Filtrage des None
    parts = [row['atlas_organism_part'] for row in parts_rows if row['atlas_organism_part'] is not None]

    conn.close()

    return render_template('gene_detail.html', gene=gene, transcripts=transcripts, parts=parts)




@app.route('/genes/<id>/edit', methods=['GET', 'POST'])
def edit_gene(id):
    conn = get_db_connection()
    gene = conn.execute('SELECT * FROM Genes WHERE ensembl_gene_id = ?', (id,)).fetchone()
    if gene is None:
        conn.close()
        return f"Gène {id} non trouvé.", 404

    if request.method == 'POST':
        new_name = request.form['associated_gene_name']
        if not new_name:
            flash('Le nom du gène est obligatoire.')
        else:
            conn.execute('UPDATE Genes SET associated_gene_name = ? WHERE ensembl_gene_id = ?', (new_name, id))
            conn.commit()
            conn.close()
            return redirect(url_for('gene_detail', id=id))

    conn.close()
    return render_template('edit_gene.html', gene=gene)

@app.route('/transcripts/<id>')
def transcript_detail(id):
    conn = get_db_connection()

    # 1. Récupération du transcrit
    transcript_row = conn.execute(
        'SELECT * FROM Transcripts WHERE Ensembl_Transcript_ID = ? limit 50', (id,)
    ).fetchone()

    if transcript_row is None:
        conn.close()
        return f"Transcrit {id} non trouvé.", 404

    transcript = dict(transcript_row)

    # 2. Récupération du gène associé via Ensembl_Gene_ID
    gene_id = transcript['Ensembl_Gene_ID']
    gene_row = conn.execute(
        'SELECT * FROM Genes WHERE Ensembl_Gene_ID = ? limit 50', (gene_id,)
    ).fetchone()
    gene = dict(gene_row) if gene_row else None

    # 3. Récupération des parties d’organismes liées à ce transcrit
    part_rows = conn.execute('''
        SELECT DISTINCT atlas_organism_part
        FROM Expression
        WHERE Ensembl_Transcript_ID = ?
        ORDER BY atlas_organism_part
        limit 50
    ''', (id,)).fetchall()

    parts = [row['atlas_organism_part'] for row in part_rows if row['atlas_organism_part']]

    conn.close()

    return render_template(
        'transcript_detail.html',
        transcript=transcript,
        gene=gene,
        parts=parts
    )



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
