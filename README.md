# MeshParser



      ============= MeshParser v2.0 =================
     | Find the disease name for input keyword      |
     | - enable tree structure for down search      |
     | - added disease name partial search          |
      ===============================================
      
     Usage : python MeshParser_v2.py MeSH(xml) keyword direction result_type show_path
             * keyword     : category or disease name in MeSH / whole / whole-path / -partial
             * direction   : up(categories) / down(dieseases)
             * result_type : all / unique (for direction down only)
             * show_path   : yes / no

Required : MeSH(xml) should be downloaded to your machine before use
          ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/xmlmesh/desc2017.xml
          
          
Example :

      1. To Find a tree structure for given keyword(disease name or unique id)
         : python MeshParser_v2.py desc2017.xml Hemianopsia up all yes
         
         (Nervous System Diseases : D009422) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Vision Disorders : D014786) >  [Hemianopsia : D006423]
        (Eye Diseases : D005128) >  (Vision Disorders : D014786) >  (Blindness : D001766) >  [Hemianopsia : D006423]
        (Pathological Conditions, Signs and Symptoms : D013568) >  (Signs and Symptoms : D012816) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Vision Disorders : D014786) >  [Hemianopsia : D006423]

         : python MeshParser_v2.py desc2017.xml D006423 up all yes         
           same result as above
           
      2. To find a disease name for some category (name or unique id) without tree path
         : python MeshParser_v2.py desc2017.xml "Sensation Disorders" down all no
         
          Olfaction Disorders (D000857)
          Hyperesthesia (D006941)
          Paresthesia (D010292)
          Hypesthesia (D006987)
          Hyperalgesia (D006930)
          Dysgeusia (D004408)
          Ageusia (D000370)
          Diplopia (D004172)
          Amblyopia (D000550)
          ...
      
         : python MeshParser_v2.py desc2017.xml "Sensation Disorders" down unique no
          same result as above but no duplilcated disease name
          
       3. To find a disease name for some category (name or unique id) with tree path
         : python MeshParser_v2.py desc2017.xml "Sensation Disorders" down all yes
         
         (Nervous System Diseases : D009422) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  [Olfaction Disorders : D000857]
          (Pathological Conditions, Signs and Symptoms : D013568) >  (Signs and Symptoms : D012816) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  [Olfaction Disorders : D000857]
          (Nervous System Diseases : D009422) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Somatosensory Disorders : D020886) >  [Hyperesthesia : D006941]
          (Pathological Conditions, Signs and Symptoms : D013568) >  (Signs and Symptoms : D012816) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Somatosensory Disorders : D020886) >  [Hyperesthesia : D006941]
          (Nervous System Diseases : D009422) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Somatosensory Disorders : D020886) >  [Paresthesia : D010292]
          (Pathological Conditions, Signs and Symptoms : D013568) >  (Signs and Symptoms : D012816) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Somatosensory Disorders : D020886) >  [Paresthesia : D010292]
          (Nervous System Diseases : D009422) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Somatosensory Disorders : D020886) >  [Hypesthesia : D006987]
          (Pathological Conditions, Signs and Symptoms : D013568) >  (Signs and Symptoms : D012816) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Somatosensory Disorders : D020886) >  [Hypesthesia : D006987]
         ...
         
       4. To find whole tree for MeSH
         : python MeshParser_v2.py desc2017.xml whole-path down all yes
         
       5. To find whole disease name for MeSH
         : python MeshParser_v2.py desc2017.xml whole down all yes         
         
       6. Find whole path using partial disease name (put keyword after '-')
         : python MeshParser_v2.py desc2017.xml -disorder down all yes
         
         (Musculoskeletal Diseases : D009140) >  (Bone Diseases : D001847) >  (Bone Diseases, Metabolic : D001851) >  (Rickets : D012279) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Male Urogenital Diseases : D052801) >  (Urologic Diseases : D014570) >  (Kidney Diseases : D007674) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Female Urogenital Diseases and Pregnancy Complications : D005261) >  (Female Urogenital Diseases : D052776) >  (Urologic Diseases : D014570) >  (Kidney Diseases : D007674) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Nutritional and Metabolic Diseases : D009750) >  (Metabolic Diseases : D008659) >  (Bone Diseases, Metabolic : D001851) >  (Rickets : D012279) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Nutritional and Metabolic Diseases : D009750) >  (Metabolic Diseases : D008659) >  (Calcium Metabolism Disorders : D002128) >  (Rickets : D012279) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Nutritional and Metabolic Diseases : D009750) >  (Nutrition Disorders : D009748) >  (Malnutrition : D044342) >  (Deficiency Diseases : D003677) >  (Avitaminosis : D001361) >  (Vitamin D Deficiency : D014808) >  (Rickets : D012279) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Endocrine System Diseases : D004700) >  (Parathyroid Diseases : D010279) >  (Hyperparathyroidism : D006961) >  (Hyperparathyroidism, Secondary : D006962) >  [Chronic Kidney Disease-Mineral and Bone Disorder : D012080]
          (Chemically-Induced Disorders : D064419) >  (Substance-Related Disorders : D019966) >  [Tobacco Use Disorder : D014029]
          (Nervous System Diseases : D009422) >  (Sleep Wake Disorders : D012893) >  (Parasomnias : D020447) >  (REM Sleep Parasomnias : D020923) >  [REM Sleep Behavior Disorder : D020187]
          (Musculoskeletal Diseases : D009140) >  (Muscular Diseases : D009135) >  (Tendinopathy : D052256) >  (Tendon Entrapment : D053682) >  [Trigger Finger Disorder : D052582]
          (Pathological Conditions, Signs and Symptoms : D013568) >  (Pathologic Processes : D010335) >  (Menstruation Disturbances : D008599) >  (Premenstrual Syndrome : D011293) >  [Premenstrual Dysphoric Disorder : D065446]
         
