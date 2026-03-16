import numpy as np
@app.route('/history')
@login_required
def history():

    session = app.db_session()

    matches = session.query(MatchHistory).order_by(
        MatchHistory.timestamp.desc()
    ).all()

    return render_template("history.html", matches=matches)
@app.route('/api/match', methods=['POST'])
def api_match():

    file = request.files['file']

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    vec = image_to_vector(filepath, app.feature_extractor)

    session = app.db_session()
    all_fps = session.query(Fingerprint).all()

    results = []

    for fp in all_fps:
        stored_vec = np.frombuffer(fp.feature_vector, dtype=np.float32)

        score = cosine_similarity(vec, stored_vec)

        results.append({
            "name": fp.name,
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {"matches": results[:3]}

@app.route('/api/match', methods=['POST'])
def api_match():

    file = request.files['file']

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    vec = image_to_vector(filepath, app.feature_extractor)

    session = app.db_session()
    all_fps = session.query(Fingerprint).all()

    results = []

    for fp in all_fps:
        stored_vec = np.frombuffer(fp.feature_vector, dtype=np.float32)

        score = cosine_similarity(vec, stored_vec)

        results.append({
            "name": fp.name,
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {"matches": results[:3]}
